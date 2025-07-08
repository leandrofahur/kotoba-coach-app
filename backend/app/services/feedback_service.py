from Levenshtein import distance
from typing import Dict, List
from .morae_service import extract_morae, extract_morae_from_transcription, analyze_morae_errors, get_morae_feedback
from .pitch_service import analyze_comprehensive_pitch

def calculate_similarity(transcription: str, phrase: str) -> int:
    """
    Calculates Levenshtein-based similarity score between transcription and phrase.
    Returns an integer between 0 and 100.
    """
    if not transcription or not phrase:
        return 0

    max_len = max(len(transcription), len(phrase))
    if max_len == 0:
        return 100

    similarity = 1 - distance(transcription, phrase) / max_len
    return int(similarity * 100)

def label_from_score(score: int) -> str:
    if score >= 95:
        return "Perfect!"
    elif score >= 80:
        return "Great job!"
    elif score >= 60:
        return "Almost there!"
    else:
        return "Needs practice"

def analyze_comprehensive_pronunciation(expected_phrase: str, transcription: str, pitch_values: List[float]) -> Dict:
    """
    Comprehensive pronunciation analysis including morae and pitch accent errors.
    Returns detailed analysis with specific error detection and feedback.
    """
    # Basic similarity score
    similarity_score = calculate_similarity(transcription, expected_phrase)
    overall_label = label_from_score(similarity_score)
    
    # Morae analysis
    expected_morae = extract_morae(expected_phrase)
    actual_morae = extract_morae_from_transcription(transcription)
    morae_errors = analyze_morae_errors(expected_morae, actual_morae)
    morae_feedback = get_morae_feedback(morae_errors)
    
    # Pitch accent analysis (now with morae sufficiency check)
    pitch_analysis = analyze_comprehensive_pitch(expected_phrase, pitch_values, actual_morae)
    
    # Calculate weighted overall score
    morae_weight = 0.6  # Morae accuracy is more important
    pitch_weight = 0.4  # Pitch accent is secondary
    
    morae_score = morae_errors["overall_accuracy"] * 100
    pitch_score = pitch_analysis["overall_pitch_score"] if pitch_analysis["overall_pitch_score"] is not None else 0
    
    weighted_score = (morae_score * morae_weight) + (pitch_score * pitch_weight)
    
    # Determine detailed feedback
    detailed_feedback = generate_detailed_feedback(
        morae_errors, 
        pitch_analysis["pitch_analysis"], 
        similarity_score
    )
    
    return {
        "overall_score": int(weighted_score),
        "overall_label": overall_label,
        "similarity_score": similarity_score,
        "transcription": transcription,
        "expected_text": expected_phrase,
        
        # Morae analysis
        "morae_analysis": {
            "expected_morae": expected_morae,
            "actual_morae": actual_morae,
            "errors": morae_errors,
            "score": morae_score,
            "feedback": morae_feedback
        },
        
        # Pitch analysis
        "pitch_analysis": {
            "expected_accent": pitch_analysis["expected_accent"],
            "actual_pitch_contour": pitch_analysis["actual_pitch_contour"],
            "errors": pitch_analysis["pitch_analysis"]["pitch_errors"],
            "score": pitch_analysis["overall_pitch_score"],
            "feedback": pitch_analysis["pitch_analysis"].get("pitch_feedback"),
            "warning": pitch_analysis["pitch_analysis"].get("warning")
        },
        
        # Detailed feedback
        "detailed_feedback": detailed_feedback,
        "error_summary": generate_error_summary(morae_errors, pitch_analysis["pitch_analysis"])
    }

def generate_detailed_feedback(morae_errors: Dict, pitch_analysis: Dict, similarity_score: int) -> str:
    """
    Generate comprehensive feedback combining morae and pitch errors.
    """
    feedback_parts = []
    
    # Overall assessment
    if similarity_score >= 95:
        feedback_parts.append("Excellent pronunciation overall!")
    elif similarity_score >= 80:
        feedback_parts.append("Good pronunciation with some areas for improvement.")
    elif similarity_score >= 60:
        feedback_parts.append("Pronunciation needs work, but you're on the right track.")
    else:
        feedback_parts.append("Pronunciation needs significant improvement.")
    
    # Morae-specific feedback
    if morae_errors["missing_morae"]:
        missing_count = len(morae_errors["missing_morae"])
        feedback_parts.append(f"You're missing {missing_count} mora(e).")
    
    if morae_errors["extra_morae"]:
        extra_count = len(morae_errors["extra_morae"])
        feedback_parts.append(f"You're adding {extra_count} extra mora(e).")
    
    if morae_errors["incorrect_morae"]:
        incorrect_count = len(morae_errors["incorrect_morae"])
        feedback_parts.append(f"You're mispronouncing {incorrect_count} mora(e).")
    
    # Pitch-specific feedback
    if pitch_analysis["pitch_errors"]:
        pitch_error_count = len(pitch_analysis["pitch_errors"])
        feedback_parts.append(f"Your pitch accent has {pitch_error_count} error(s).")
    
    # Positive reinforcement
    if not morae_errors["error_positions"] and not pitch_analysis["pitch_errors"]:
        feedback_parts.append("Perfect morae and pitch accent!")
    
    return " ".join(feedback_parts)

def generate_error_summary(morae_errors: Dict, pitch_analysis: Dict) -> Dict:
    """
    Generate a summary of all errors for easy UI consumption.
    """
    return {
        "total_errors": len(morae_errors["error_positions"]) + len(pitch_analysis["pitch_errors"]),
        "morae_error_count": len(morae_errors["error_positions"]),
        "pitch_error_count": len(pitch_analysis["pitch_errors"]),
        "missing_morae_count": len(morae_errors["missing_morae"]),
        "extra_morae_count": len(morae_errors["extra_morae"]),
        "incorrect_morae_count": len(morae_errors["incorrect_morae"]),
        "has_errors": len(morae_errors["error_positions"]) > 0 or len(pitch_analysis["pitch_errors"]) > 0
    }

def get_improvement_suggestions(morae_errors: Dict, pitch_analysis: Dict) -> List[str]:
    """
    Generate specific improvement suggestions based on detected errors.
    """
    suggestions = []
    
    # Morae suggestions
    if morae_errors["missing_morae"]:
        suggestions.append("Practice elongating sounds to include all morae.")
    
    if morae_errors["extra_morae"]:
        suggestions.append("Be careful not to add extra sounds between morae.")
    
    if morae_errors["incorrect_morae"]:
        suggestions.append("Focus on the correct pronunciation of individual morae.")
    
    # Pitch suggestions
    if pitch_analysis["pitch_errors"]:
        suggestions.append("Pay attention to pitch accent patterns - practice with native speakers.")
    
    if not suggestions:
        suggestions.append("Great job! Keep practicing to maintain your excellent pronunciation.")
    
    return suggestions


