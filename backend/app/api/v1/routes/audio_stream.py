from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import tempfile
import os
import subprocess
from pathlib import Path
from services.whisper_service import transcribe_audio
from services.feedback_service import analyze_comprehensive_pronunciation
from services.pitch_service import extract_pitch_librosa
from services.phrase_service import get_phrase_by_id

router = APIRouter(prefix="/audio-stream", tags=["Audio Stream"])

# Add this new endpoint for audio file streaming
@router.get("/audio/{lesson_id}")
async def stream_audio_file(lesson_id: str):
    # Get the lesson phrase
    phrase = get_phrase_by_id(lesson_id)
    if not phrase:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Get the audio file path
    audio_path = Path(f"app{phrase.audio_url}")
    
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    # Stream the audio file
    def audio_generator():
        with open(audio_path, "rb") as audio_file:
            while chunk := audio_file.read(8192):  # Read in 8KB chunks
                yield chunk
    
    return StreamingResponse(
        audio_generator(),
        media_type="audio/wav",
        headers={"Content-Disposition": f"attachment; filename=lesson_{lesson_id}.wav"}
    )

@router.websocket("/ws/{lesson_id}")
async def audio_stream_websocket(websocket: WebSocket, lesson_id: str):
    await websocket.accept()
    
    # Get the lesson phrase
    phrase = get_phrase_by_id(lesson_id)
    if not phrase:
        await websocket.send_json({"error": "Lesson not found"})
        return
    
    audio_chunks = []
    chunk_count = 0
    
    try:
        while True:
            # Receive data - could be binary audio or JSON message
            message = await websocket.receive()
            
            # Check if it's text (JSON) or binary data
            if "text" in message:
                # Handle JSON message (like stop signal)
                try:
                    data = message["text"]
                    print(f"Received text message: {data}")
                    if data == '{"action":"stop"}':
                        print("Received stop signal, processing final audio...")
                        break
                except:
                    pass
            elif "bytes" in message:
                # Handle binary audio data
                audio_chunk = message["bytes"]
                print(f"Received binary chunk: {len(audio_chunk)} bytes")
                
                audio_chunks.append(audio_chunk)
                chunk_count += 1
                
                # Send immediate acknowledgment
                await websocket.send_json({
                    "status": "chunk_received",
                    "chunk_size": len(audio_chunk),
                    "total_chunks": chunk_count
                })
        
        # Process ALL accumulated chunks when stop signal is received
        if audio_chunks:
            await process_complete_audio(audio_chunks, phrase, websocket)
            
    except WebSocketDisconnect:
        print(f"Client disconnected from lesson {lesson_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({
            "status": "error", 
            "message": str(e)
        })

async def process_complete_audio(audio_chunks, phrase, websocket):
    try:
        # Combine ALL accumulated chunks into one complete WebM file
        complete_audio = b''.join(audio_chunks)
        print(f"Processing complete audio: {len(complete_audio)} bytes")
        print(f"First 50 bytes: {complete_audio[:50]}")
        
        # Save complete WebM audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_webm:
            temp_webm.write(complete_audio)
            temp_webm_path = temp_webm.name
        
        print(f"Saved complete WebM file: {temp_webm_path}")
        
        # Convert complete WebM to WAV using FFmpeg
        temp_wav_path = temp_webm_path.replace('.webm', '.wav')
        
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", temp_webm_path,
            "-ac", "1",         # mono
            "-ar", "16000",     # 16kHz
            temp_wav_path
        ]
        
        print(f"Running FFmpeg command: {' '.join(ffmpeg_cmd)}")
        
        try:
            result = subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("FFmpeg conversion successful")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            raise RuntimeError(f"Audio conversion failed: {e.stderr.decode()}") from e
        
        # Process with comprehensive analysis using the converted WAV file
        transcription = transcribe_audio(temp_wav_path)
        pitch_contour = extract_pitch_librosa(temp_wav_path)
        
        # Comprehensive pronunciation analysis
        analysis = analyze_comprehensive_pronunciation(
            expected_phrase=phrase.text,
            transcription=transcription,
            pitch_values=pitch_contour
        )
        
        print(f"Processing results - Overall Score: {analysis['overall_score']}%, Transcription: {transcription}")
        
        # Send comprehensive feedback
        await websocket.send_json({
            "status": "feedback",
            **analysis  # Include all analysis results
        })
        
        # Clean up temp files
        os.unlink(temp_webm_path)
        os.unlink(temp_wav_path)
        
    except Exception as e:
        print(f"Processing error: {e}")
        await websocket.send_json({
            "status": "error",
            "message": f"Processing error: {str(e)}"
        }) 