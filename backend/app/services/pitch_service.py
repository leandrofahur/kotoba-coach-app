# import parselmouth
# import numpy as np

# def extract_pitch_contour(wav_path: str, time_step: float = 0.01) -> list[float]:
#     """
#     Extract pitch (F0 in Hz) at regular intervals from the audio file.
#     """
#     snd = parselmouth.Sound(wav_path)
#     pitch = snd.to_pitch(time_step=time_step)
#     pitch_values = []

#     for i in range(pitch.get_number_of_frames()):
#         f0 = pitch.get_value_in_frame(i)
#         pitch_values.append(f0 if f0 is not None else 0.0)

#     return pitch_values

# def extract_pitch_accents(phrase: str):
#     """
#     Extracts pitch accent information using pyopenjtalk.
#     Returns a list of mora entries with pitch and accent info.
#     """
#     labels = pyopenjtalk.run_frontend(phrase)
#     pitch_info = []

#     for label in labels:
#         parts = label.split('/')
#         # Parse useful fields
#         a_match = [p for p in parts if "A:" in p]
#         f_match = [p for p in parts if "F:" in p]
#         g_match = [p for p in parts if "G:" in p]

#         try:
#             accent_type = int(a_match[0].split(':')[1].split('_')[0])
#             accent_pos = int(f_match[0].split(':')[1].split('_')[0])
#             accent_total = int(g_match[0].split(':')[1].split('_')[0])

#             pitch_info.append({
#                 "accent_type": accent_type,
#                 "accent_position": accent_pos,
#                 "accent_total": accent_total
#             })

#         except Exception as e:
#             print(f"Error parsing label: {label} -> {e}")
#             continue

#     return pitch_info

# def derive_pitch_pattern(accent_type: int, total: int) -> list[str]:
#     # Japanese pitch starts low, so we start with "L"
#     pattern = ["L"]
#     for i in range(1, total):
#         if i < accent_type:
#             pattern.append("H")
#         elif i == accent_type:
#             pattern.append("L")
#         else:
#             pattern.append("L")
#     return pattern

import librosa
import numpy as np
import math
import pyopenjtalk
from typing import List, Dict, Tuple, Optional

# Japanese pitch accent dictionary for common phrases
PITCH_ACCENT_DICT = {
    # Heiban (flat accent) phrases
    "こんにちは": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L"]},
    "おはよう": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L"]},
    "おはようございます": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L", "L", "L", "L"]},
    "こんばんは": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L"]},
    "ありがとう": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L"]},
    "さようなら": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L"]},
    "おやすみ": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L"]},
    "いただきます": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L"]},
    "ごちそうさま": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L"]},
    "はじめまして": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L"]},
    "よろしく": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L"]},
    "おねがいします": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L", "L"]},
    "すみません": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L"]},
    "わかりました": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L", "L", "L"]},
    "がんばって": {"type": 0, "name": "heiban (flat)", "pattern": ["L", "L", "L"]},
    
    # Atamadaka (head-high) phrases
    "はし": {"type": 1, "name": "atamadaka (head-high)", "pattern": ["H", "L"]},  # bridge
    "はな": {"type": 1, "name": "atamadaka (head-high)", "pattern": ["H", "L"]},  # flower
    "みず": {"type": 1, "name": "atamadaka (head-high)", "pattern": ["H", "L"]},  # water
    "かみ": {"type": 1, "name": "atamadaka (head-high)", "pattern": ["H", "L"]},  # paper
    "あめ": {"type": 1, "name": "atamadaka (head-high)", "pattern": ["H", "L"]},  # rain
    
    # Nakadaka (middle-high) phrases
    "あたま": {"type": 2, "name": "nakadaka (middle-high)", "pattern": ["L", "H", "L"]},  # head
    "おとこ": {"type": 2, "name": "nakadaka (middle-high)", "pattern": ["L", "H", "L"]},  # man
    "おんな": {"type": 2, "name": "nakadaka (middle-high)", "pattern": ["L", "H", "L"]},  # woman
    "かばん": {"type": 2, "name": "nakadaka (middle-high)", "pattern": ["L", "H", "L"]},  # bag
    "でんわ": {"type": 2, "name": "nakadaka (middle-high)", "pattern": ["L", "H", "L"]},  # phone
    
    # Odaka (tail-high) phrases
    "あめ": {"type": 3, "name": "odaka (tail-high)", "pattern": ["L", "H"]},  # candy (different from rain)
    "ゆき": {"type": 3, "name": "odaka (tail-high)", "pattern": ["L", "H"]},  # snow
    "ほし": {"type": 3, "name": "odaka (tail-high)", "pattern": ["L", "H"]},  # star
    "つき": {"type": 3, "name": "odaka (tail-high)", "pattern": ["L", "H"]},  # moon
    "かみ": {"type": 3, "name": "odaka (tail-high)", "pattern": ["L", "H"]},  # hair (different from paper)
}

def extract_pitch_librosa(audio_path: str, sr: int = 16000) -> List[float]:
    """
    Extract pitch (F0 in Hz) using librosa's pyin algorithm.
    Returns a list of float pitch values (0.0 where unvoiced or invalid).
    """
    y, sr = librosa.load(audio_path, sr=sr)

    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=sr
    )

    # Replace NaNs or invalid values with 0.0
    pitch_values = []
    for val in f0:
        if val is None or not math.isfinite(val):
            pitch_values.append(0.0)
        else:
            pitch_values.append(float(val))

    return pitch_values

def extract_pitch_accent_info(phrase: str) -> Dict:
    """
    Extract pitch accent information using dictionary lookup and morae analysis.
    Returns detailed accent information for the phrase.
    """
    try:
        # First, try to get accent info from our dictionary
        if phrase in PITCH_ACCENT_DICT:
            accent_data = PITCH_ACCENT_DICT[phrase]
            morae = pyopenjtalk.g2p(phrase).split(" ")
            return {
                "accent_type": accent_data["type"],
                "accent_position": 0,  # For heiban, position is 0
                "total_morae": len(morae),
                "pitch_pattern": accent_data["pattern"],
                "accent_details": [{
                    "accent_type": accent_data["type"],
                    "accent_position": 0,
                    "accent_total": len(morae)
                }]
            }
        
        # If not in dictionary, use morae count and default to heiban
        morae = pyopenjtalk.g2p(phrase).split(" ")
        total_morae = len(morae)
        
        # Generate a reasonable pattern based on morae count
        pattern = ["L"] * total_morae  # Default to all low for heiban
        
        return {
            "accent_type": 0,  # heiban (flat)
            "accent_position": 0,
            "total_morae": total_morae,
            "pitch_pattern": pattern,
            "accent_details": [{
                "accent_type": 0,
                "accent_position": 0,
                "accent_total": total_morae
            }]
        }
        
    except Exception as e:
        print(f"Error extracting pitch accent info: {e}")
        # Fallback: return basic info
        return {
            "accent_type": 0,
            "accent_position": 0,
            "total_morae": 0,
            "pitch_pattern": [],
            "accent_details": []
        }

def derive_pitch_pattern(accent_type: int, total: int) -> List[str]:
    """
    Derive expected pitch pattern based on accent type and total morae.
    Returns a list of "H" (high) and "L" (low) pitch markers.
    """
    if total == 0:
        return []
    
    # Japanese pitch starts low, so we start with "L"
    pattern = ["L"]
    
    for i in range(1, total):
        if accent_type == 0:
            # Flat accent (heiban) - all low
            pattern.append("L")
        elif i < accent_type:
            # Before accent peak - high
            pattern.append("H")
        elif i == accent_type:
            # At accent peak - low (falling)
            pattern.append("L")
        else:
            # After accent peak - low
            pattern.append("L")
    
    return pattern

def analyze_pitch_contour(pitch_values: List[float], expected_pattern: List[str]) -> Dict:
    """
    Analyze pitch contour against expected pattern.
    Returns pitch error analysis with improved logic.
    """
    if not pitch_values or not expected_pattern:
        return {
            "pitch_errors": [],
            "overall_pitch_accuracy": 0.0,
            "pitch_feedback": "Unable to analyze pitch"
        }
    
    # Segment pitch values into morae (improved approach)
    morae_count = len(expected_pattern)
    if morae_count == 0:
        return {
            "pitch_errors": [],
            "overall_pitch_accuracy": 0.0,
            "pitch_feedback": "No morae to analyze"
        }
    
    # Use a more sophisticated segmentation approach
    pitch_errors = []
    correct_pitch_count = 0
    
    # Calculate pitch statistics for better analysis
    valid_pitches = [p for p in pitch_values if p > 0]
    if not valid_pitches:
        return {
            "pitch_errors": [],
            "overall_pitch_accuracy": 0.0,
            "pitch_feedback": "No voiced sounds detected"
        }
    
    # For heiban (flat accent), be more lenient since it's all low pitch
    # Japanese pitch accent is subtle, so we need to account for natural variations
    pitch_mean = np.mean(valid_pitches)
    pitch_std = np.std(valid_pitches)
    
    # More lenient thresholds for heiban analysis
    # Since heiban is all low, we're mainly looking for obvious high pitches
    high_threshold = pitch_mean + 1.0 * pitch_std  # More lenient threshold
    
    # Segment pitch values into morae
    segment_size = max(1, len(pitch_values) // morae_count)
    
    for i in range(morae_count):
        start_idx = i * segment_size
        end_idx = start_idx + segment_size if i < morae_count - 1 else len(pitch_values)
        
        # Get pitch values for this mora
        mora_pitch_values = pitch_values[start_idx:end_idx]
        valid_mora_pitches = [p for p in mora_pitch_values if p > 0]
        
        if not valid_mora_pitches:
            # No voiced sound in this mora - this is acceptable for heiban
            correct_pitch_count += 1
            continue
        
        # Calculate mora pitch characteristics
        mora_mean = np.mean(valid_mora_pitches)
        mora_max = np.max(valid_mora_pitches)
        
        # For heiban (all low), we're looking for obvious high pitches that shouldn't be there
        # Be more lenient - only flag if it's clearly too high
        is_obviously_high = mora_mean > high_threshold and mora_max > pitch_mean + 1.5 * pitch_std
        expected_high = expected_pattern[i] == "H"
        
        if expected_high:
            # If we expect high pitch, check if it's high enough
            is_high_enough = mora_mean > pitch_mean + 0.5 * pitch_std
            if is_high_enough:
                correct_pitch_count += 1
            else:
                pitch_errors.append({
                    "position": i,
                    "expected": expected_pattern[i],
                    "actual": "L",
                    "error_type": "missing_high_pitch",
                    "pitch_value": mora_mean,
                    "threshold": pitch_mean + 0.5 * pitch_std
                })
        else:
            # For low pitch (heiban), only flag if it's obviously too high
            if is_obviously_high:
                pitch_errors.append({
                    "position": i,
                    "expected": expected_pattern[i],
                    "actual": "H",
                    "error_type": "wrong_pitch_level",
                    "pitch_value": mora_mean,
                    "threshold": high_threshold
                })
            else:
                correct_pitch_count += 1
    
    overall_accuracy = correct_pitch_count / morae_count if morae_count > 0 else 0.0
    
    return {
        "pitch_errors": pitch_errors,
        "overall_pitch_accuracy": overall_accuracy,
        "pitch_feedback": generate_pitch_feedback(pitch_errors, expected_pattern)
    }

def generate_pitch_feedback(pitch_errors: List[Dict], expected_pattern: List[str]) -> str:
    """
    Generate human-readable feedback based on pitch errors.
    """
    if not pitch_errors:
        return "Perfect pitch accent!"
    
    feedback_parts = []
    
    for error in pitch_errors:
        position = error["position"] + 1  # 1-indexed for user
        if error["error_type"] == "missing_high_pitch":
            feedback_parts.append(f"Mora {position}: Missing high pitch")
        elif error["error_type"] == "wrong_pitch_level":
            if error["expected"] == "H":
                feedback_parts.append(f"Mora {position}: Should be high pitch")
            else:
                feedback_parts.append(f"Mora {position}: Should be low pitch")
    
    return " | ".join(feedback_parts)

def get_pitch_accent_name(accent_type: int) -> str:
    """
    Get the name of the pitch accent pattern.
    """
    accent_names = {
        0: "heiban (flat)",
        1: "atamadaka (head-high)",
        2: "nakadaka (middle-high)",
        3: "odaka (tail-high)",
        4: "kifuku (rising-falling)"
    }
    return accent_names.get(accent_type, f"accent type {accent_type}")

def analyze_comprehensive_pitch(expected_phrase: str, actual_pitch_values: List[float]) -> Dict:
    """
    Comprehensive pitch analysis combining accent info and contour analysis.
    """
    # Get expected pitch accent information
    accent_info = extract_pitch_accent_info(expected_phrase)
    expected_pattern = accent_info["pitch_pattern"]
    
    # Analyze actual pitch contour
    contour_analysis = analyze_pitch_contour(actual_pitch_values, expected_pattern)
    
    return {
        "expected_accent": {
            "type": accent_info["accent_type"],
            "name": get_pitch_accent_name(accent_info["accent_type"]),
            "position": accent_info["accent_position"],
            "total_morae": accent_info["total_morae"],
            "pattern": expected_pattern
        },
        "actual_pitch_contour": actual_pitch_values,
        "pitch_analysis": contour_analysis,
        "overall_pitch_score": contour_analysis["overall_pitch_accuracy"] * 100
    }