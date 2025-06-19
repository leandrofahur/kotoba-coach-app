import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes the given audio file using Whisper.
    Returns the raw transcription text.
    """
    result = model.transcribe(audio_path)
    return result["text"].strip()



