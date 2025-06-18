import openai
import os
import json
import io
from typing import Dict, Tuple, Optional
import numpy as np
import tempfile
import soundfile as sf
import dotenv
from dotenv import load_dotenv


class AIAudioEvaluator:
    def __init__(self, api_key: str = None):
        """Initialize AI evaluator with OpenAI API key"""
        load_dotenv()        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            print("Warning: No OpenAI API key found. AI evaluation will be disabled.")
            self.client = None
    
    def save_audio_temp(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        """Save audio bytes to temporary file for Whisper API"""
        try:
            # Convert audio to proper format for Whisper
            import librosa
            audio_array, sr = librosa.load(io.BytesIO(audio_data), sr=sample_rate)
            
            # Save as temporary WAV file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            sf.write(temp_file.name, audio_array, sample_rate)
            return temp_file.name
        except Exception as e:
            print(f"Error saving audio: {e}")
            return None
    
    def evaluate_pronunciation(self, audio_file_path: str, expected_text: str = "おはようございます") -> Dict:
        """
        Evaluate pronunciation using Whisper API
        Returns: Dictionary with transcription, accuracy, and pronunciation score
        """
        if not self.client:
            return {
                "error": "No API key available",
                "score": 0,
                "transcription": "",
                "accuracy": 0
            }
        
        try:
            # Transcribe audio using Whisper
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="ja"
                )
            
            transcription = transcript.text.strip()
            
            # Calculate accuracy score
            accuracy_score = self._calculate_text_accuracy(transcription, expected_text)
            
            # Calculate pronunciation score based on transcription quality
            pronunciation_score = self._calculate_pronunciation_score(transcription, expected_text)
            
            # Clean up temporary file
            os.unlink(audio_file_path)
            
            return {
                "transcription": transcription,
                "accuracy": accuracy_score,
                "pronunciation_score": pronunciation_score,
                "expected_text": expected_text,
                "final_score": (accuracy_score + pronunciation_score) / 2
            }
            
        except Exception as e:
            print(f"Error in AI evaluation: {e}")
            # Clean up temporary file if it exists
            if os.path.exists(audio_file_path):
                os.unlink(audio_file_path)
            
            return {
                "error": str(e),
                "score": 0,
                "transcription": "",
                "accuracy": 0
            }
    
    def _calculate_text_accuracy(self, transcription: str, expected: str) -> float:
        """Calculate text accuracy using character-level comparison"""
        if not transcription or not expected:
            return 0.0
        
        # Normalize text (remove spaces, convert to lowercase for comparison)
        trans_norm = ''.join(transcription.lower().split())
        expected_norm = ''.join(expected.lower().split())
        
        if not expected_norm:
            return 0.0
        
        # Calculate character-level accuracy
        correct_chars = sum(1 for a, b in zip(trans_norm, expected_norm) if a == b)
        total_chars = len(expected_norm)
        
        # Bonus for length similarity
        length_ratio = min(len(trans_norm), len(expected_norm)) / max(len(trans_norm), len(expected_norm))
        
        accuracy = (correct_chars / total_chars) * 0.8 + length_ratio * 0.2
        return min(100, accuracy * 100)
    
    def _calculate_pronunciation_score(self, transcription: str, expected: str) -> float:
        """Calculate pronunciation score based on transcription quality"""
        if not transcription:
            return 0.0
        
        # Base score from transcription quality
        base_score = 50.0
        
        # Bonus for getting the right phrase
        if expected.lower() in transcription.lower():
            base_score += 30
        
        # Bonus for transcription length (indicates speech was detected)
        if len(transcription) > 3:
            base_score += 10
        
        # Bonus for Japanese characters detected
        japanese_chars = sum(1 for char in transcription if '\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff')
        if japanese_chars > 0:
            base_score += 10
        
        return min(100, base_score)

# Global evaluator instance
ai_evaluator = None

def initialize_ai_evaluator(api_key: str = None):
    """Initialize the global AI evaluator"""
    global ai_evaluator
    ai_evaluator = AIAudioEvaluator(api_key)

def get_ai_evaluation(audio_data: bytes, expected_text: str = "おはようございます") -> Dict:
    """Get AI evaluation for audio data"""
    global ai_evaluator
    
    if not ai_evaluator:
        return {
            "error": "AI evaluator not initialized",
            "score": 0,
            "transcription": "",
            "accuracy": 0
        }
    
    # Save audio to temporary file
    temp_file = ai_evaluator.save_audio_temp(audio_data)
    if not temp_file:
        return {
            "error": "Failed to process audio",
            "score": 0,
            "transcription": "",
            "accuracy": 0
        }
    
    # Get evaluation
    return ai_evaluator.evaluate_pronunciation(temp_file, expected_text) 