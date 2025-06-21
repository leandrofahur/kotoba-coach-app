import { useNavigate, useLocation, useParams, Navigate } from "react-router-dom";
import { X, Snail, Volume1, Bookmark, Mic } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { useAudioStream } from "@/hooks/useAudioStream";
import { useState, useEffect, useRef } from "react";
import type { LessonBlockProps } from "@/components/LessonBlock/LessonBlock.types";

function Study() {
    const navigate = useNavigate();
    const location = useLocation();
    const { id } = useParams<{ id: string }>();
    const lesson = location.state?.lesson as LessonBlockProps | undefined;
    const [isRecording, setIsRecording] = useState(false);
    const [pronunciationScore, setPronunciationScore] = useState<number | null>(null);
    const [transcription, setTranscription] = useState<string>("");
    const [feedback, setFeedback] = useState<string>("");
    const [isProcessing, setIsProcessing] = useState(false);
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    const { startStreaming, stopStreaming } = useAudioStream(id!);

    // Listen for pronunciation feedback
    useEffect(() => {
        const handleFeedback = (event: CustomEvent) => {
            const data = event.detail;
            console.log('Received feedback in Study component:', data);
            
            if (data.status === 'feedback') {
                setPronunciationScore(data.score);
                setTranscription(data.transcription);
                setFeedback(data.label);
                setIsProcessing(false);
            } else if (data.status === 'chunk_received') {
                setIsProcessing(true);
            }
        };

        window.addEventListener('pronunciationFeedback', handleFeedback as EventListener);
        
        return () => {
            window.removeEventListener('pronunciationFeedback', handleFeedback as EventListener);
        };
    }, []);

    // Redirect if no lesson data or ID mismatch
    if (!lesson || lesson.id !== id) {
        return <Navigate to="/lessons" />;
    }

    const handleBack = () => {
        navigate("/lessons");
    }

    const handlePlay = async () => {
        if (!lesson) return;
        
        try {
            setIsPlaying(true);
            
            // Create audio element if it doesn't exist
            if (!audioRef.current) {
                audioRef.current = new Audio();
                
                audioRef.current.onended = () => {
                    setIsPlaying(false);
                };
                
                audioRef.current.onerror = () => {
                    console.error('Audio playback error');
                    setIsPlaying(false);
                };
            }
            
            // Set the audio source
            audioRef.current.src = `http://localhost:8000/api/v1/audio-stream/audio/${lesson.id}`;
            
            // Play the audio
            await audioRef.current.play();
            console.log('Playing teacher audio');
            
        } catch (error) {
            console.error('Error playing audio:', error);
            setIsPlaying(false);
        }
    }

    const handleSlowPlay = async () => {
        if (!lesson) return;
        
        try {
            setIsPlaying(true);
            
            // Create audio element if it doesn't exist
            if (!audioRef.current) {
                audioRef.current = new Audio();
                
                audioRef.current.onended = () => {
                    setIsPlaying(false);
                };
                
                audioRef.current.onerror = () => {
                    console.error('Audio playback error');
                    setIsPlaying(false);
                };
            }
            
            // Set the audio source
            audioRef.current.src = `http://localhost:8000/api/v1/audio-stream/audio/${lesson.id}`;
            
            // Set playback rate for slow play
            audioRef.current.playbackRate = 0.5;
            
            // Play the audio
            await audioRef.current.play();
            console.log('Playing teacher audio (slow)');
            
        } catch (error) {
            console.error('Error playing audio:', error);
            setIsPlaying(false);
        }
    }

    const handleBookmark = () => {
        console.log("bookmark", lesson.id);
    }

    const handleSpeak = async () => {
        console.log('Speak button clicked, current state:', { isRecording });
        
        if (!isRecording) {
            // Start recording
            console.log('Starting recording...');
            setIsRecording(true);
            setFeedback("Listening...");
            setPronunciationScore(null);
            setTranscription("");
            try {
                await startStreaming();
                console.log('Recording started successfully');
            } catch (error) {
                console.error('Failed to start recording:', error);
                setIsRecording(false);
                setFeedback("Error starting recording");
            }
        } else {
            // Stop recording
            console.log('Stopping recording...');
            setIsRecording(false);
            setFeedback("Processing...");
            setIsProcessing(true);
            stopStreaming();
            console.log('Recording stopped');
        }
    }

    return (
        <div className="flex flex-col h-screen w-full bg-beige-light">
            <div className="flex flex-col p-4 h-1/2">
                <div className="flex items-center">
                    <X className="w-8 h-8" onClick={handleBack} />
                    <Progress value={75} className="w-full ml-4"/>
                </div>
                <div className="flex flex-col w-full mt-4 h-full">
                    <p className="text-start text-[12px] font-[600] text-black-dark">Repeat After Me</p>
                    <div className="flex justify-center items-center h-full">
                        <div className="bg-gray-xlight w-[210px] h-[210px] rounded-full"/>                                            
                    </div>
                </div>                                
            </div>                        
            
            <div className="flex flex-col bg-white p-4 border rounded-t-2xl border-gray-light h-1/2">
                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <span className="bg-black-dark h-4 w-4 rounded-full mr-2" />
                        <p className="text-[12px] leading-6">Score</p>
                    </div>
                    <div className="flex items-center">                        
                        <p className="text-[16px] leading-6">
                            {pronunciationScore !== null ? `${pronunciationScore}%` : ''}
                        </p>
                    </div>
                </div>    

                <p className="text-[32px] font-bold mt-4">{lesson.text}</p>
                <p className="text-[12px] font-bold mt-2">{lesson.translation}</p>
                
                {/* Show transcription and feedback */}
                {transcription && (
                    <div className="mt-2 p-2 bg-gray-100 rounded">
                        <p className="text-sm text-gray-600">You said: {transcription}</p>
                        <p className="text-sm font-medium text-primary">{feedback}</p>
                    </div>
                )}
                
                {/* Show processing status */}
                {isProcessing && (
                    <div className="mt-2 p-2 bg-blue-100 rounded">
                        <p className="text-sm text-blue-600">Processing your pronunciation...</p>
                    </div>
                )}
                
                <div className="flex items-center gap-4 mt-4">                    
                    <Volume1 
                        className={`size-7 ${isPlaying ? 'text-green-500' : 'text-primary'}`} 
                        onClick={handlePlay}
                    />
                    <Snail 
                        className={`size-7 ${isPlaying ? 'text-green-500' : 'text-primary'}`} 
                        onClick={handleSlowPlay}
                    />                    
                    <Bookmark className="text-primary size-7" onClick={handleBookmark}/>                    
                </div>
                
                <div className="flex flex-col items-center justify-center h-full gap-2">
                    <Button 
                        className={`w-[60px] h-[60px] rounded-full ${isRecording ? 'bg-red-500 hover:bg-red-600' : ''}`} 
                        onClick={handleSpeak}
                    >
                        <Mic className="size-6" />
                    </Button>
                    {feedback && !transcription && (
                        <p className="text-sm text-gray-600">{feedback}</p>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Study;