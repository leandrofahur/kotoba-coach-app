import tempfile
import io
import librosa
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity

ASSET_PATH = Path(__file__).resolve().parent.parent / "assets" / "audio" / "ohayougozaimasu.mp3"

def validate_audio(audio: np.ndarray, sr: int) -> bool:
    """
    Validate audio quality and detect silent/empty audio
    Returns: True if audio is valid, False otherwise
    """
    # Check for silent audio
    if np.max(np.abs(audio)) < 0.01:  # Very low amplitude threshold
        return False
    
    # Check for zero variance
    if np.var(audio) < 1e-6:
        return False
    
    # Check minimum duration (at least 0.5 seconds)
    if len(audio) / sr < 0.5:
        return False
    
    return True

def process_audio_in_memory(audio_data: bytes) -> Optional[Tuple[np.ndarray, int]]:
    """
    Process uploaded audio data directly in memory
    Returns: (Audio array, sample rate) for librosa processing
    """
    try:
        # Convert bytes to audio array
        audio_array, sr = librosa.load(io.BytesIO(audio_data), sr=None)
        
        # Validate audio quality
        if not validate_audio(audio_array, sr):
            return None
            
        return audio_array, sr
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

def extract_mfcc_features(audio: np.ndarray, sr: int, n_mfcc: int = 13) -> np.ndarray:
    """
    Extract MFCC features from audio
    Args:
        audio: Audio array
        sr: Sample rate
        n_mfcc: Number of MFCC coefficients (default 13 for speech)
    Returns: MFCC feature matrix
    """
    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    
    # Safe normalization with better handling of edge cases
    mfcc_mean = np.mean(mfcc, axis=1, keepdims=True)
    mfcc_std = np.std(mfcc, axis=1, keepdims=True)
    
    # Avoid division by zero and handle very small std values
    mfcc_std = np.maximum(mfcc_std, 1e-8)
    mfcc_normalized = (mfcc - mfcc_mean) / mfcc_std
    
    return mfcc_normalized

def align_features(feature1: np.ndarray, feature2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Align two feature matrices to same length for comparison
    Uses the shorter length and truncates the longer one
    """
    min_length = min(feature1.shape[1], feature2.shape[1])
    return feature1[:, :min_length], feature2[:, :min_length]

def calculate_similarity_score(user_audio: np.ndarray, user_sr: int, 
                             reference_audio: np.ndarray, reference_sr: int) -> float:
    """
    Calculate similarity score between user and reference audio using MFCC
    Returns: Score between 0-100 with improved scaling
    """
    try:
        # Extract MFCC features from both audios
        user_mfcc = extract_mfcc_features(user_audio, user_sr)
        reference_mfcc = extract_mfcc_features(reference_audio, reference_sr)
        
        # Align features to same length
        user_mfcc_aligned, ref_mfcc_aligned = align_features(user_mfcc, reference_mfcc)
        
        # Calculate cosine similarity for each MFCC coefficient
        similarities = []
        for i in range(user_mfcc_aligned.shape[0]):
            user_coeff = user_mfcc_aligned[i].reshape(1, -1)
            ref_coeff = ref_mfcc_aligned[i].reshape(1, -1)
            
            # Calculate cosine similarity
            sim = cosine_similarity(user_coeff, ref_coeff)[0][0]
            similarities.append(float(sim))
        
        # Average similarity across all coefficients
        avg_similarity = np.mean(similarities)
        
        # Improved scoring function for demo purposes
        # This creates more dramatic differences and handles edge cases better
        if avg_similarity <= 0:
            score = 0
        elif avg_similarity >= 0.8:
            score = 90 + (avg_similarity - 0.8) * 50  # 90-100 for excellent
        elif avg_similarity >= 0.6:
            score = 70 + (avg_similarity - 0.6) * 100  # 70-90 for good
        elif avg_similarity >= 0.4:
            score = 40 + (avg_similarity - 0.4) * 150  # 40-70 for average
        else:
            score = avg_similarity * 100  # 0-40 for poor
        
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
        return round(float(score), 2)
        
    except Exception as e:
        print(f"Error calculating similarity score: {e}")
        return 0.0

def load_reference_audio() -> Tuple[np.ndarray, int]:
    """Load reference audio for comparison"""
    audio_array, sr = librosa.load(str(ASSET_PATH), sr=None)
    return audio_array, sr