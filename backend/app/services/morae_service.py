import pyopenjtalk
from typing import List, Dict, Tuple
import re

def extract_morae(phrase: str) -> List[str]:
    """
    Converts a Japanese phrase into a list of morae (hiragana units).
    """
    g2p_hiragana = pyopenjtalk.g2p(phrase)
    return g2p_hiragana.split(" ")

def extract_morae_from_transcription(transcription: str) -> List[str]:
    """
    Extract morae from user's transcription using the same method.
    """
    g2p_hiragana = pyopenjtalk.g2p(transcription)
    return g2p_hiragana.split(" ")

def analyze_morae_errors(expected_morae: List[str], actual_morae: List[str]) -> Dict:
    """
    Analyze morae errors by comparing expected vs actual morae.
    Returns detailed error analysis including missing, extra, and incorrect morae.
    """
    errors = {
        "missing_morae": [],
        "extra_morae": [],
        "incorrect_morae": [],
        "overall_accuracy": 0.0,
        "error_positions": []
    }
    
    # Find the longer list for comparison
    max_length = max(len(expected_morae), len(actual_morae))
    
    # Pad shorter list with None for comparison
    expected_padded = expected_morae + [None] * (max_length - len(expected_morae))
    actual_padded = actual_morae + [None] * (max_length - len(actual_morae))
    
    correct_count = 0
    
    for i, (expected, actual) in enumerate(zip(expected_padded, actual_padded)):
        if expected is None and actual is not None:
            # Extra mora
            errors["extra_morae"].append({
                "position": i,
                "mora": actual,
                "expected": None
            })
            errors["error_positions"].append(i)
        elif expected is not None and actual is None:
            # Missing mora
            errors["missing_morae"].append({
                "position": i,
                "mora": None,
                "expected": expected
            })
            errors["error_positions"].append(i)
        elif expected != actual:
            # Incorrect mora
            errors["incorrect_morae"].append({
                "position": i,
                "mora": actual,
                "expected": expected
            })
            errors["error_positions"].append(i)
        else:
            # Correct mora
            correct_count += 1
    
    # Calculate overall accuracy
    if max_length > 0:
        errors["overall_accuracy"] = correct_count / max_length
    
    return errors

def get_morae_feedback(morae_errors: Dict) -> str:
    """
    Generate human-readable feedback based on morae errors.
    """
    feedback_parts = []
    
    if morae_errors["missing_morae"]:
        missing_list = [f"'{error['expected']}'" for error in morae_errors["missing_morae"]]
        feedback_parts.append(f"Missing morae: {', '.join(missing_list)}")
    
    if morae_errors["extra_morae"]:
        extra_list = [f"'{error['mora']}'" for error in morae_errors["extra_morae"]]
        feedback_parts.append(f"Extra morae: {', '.join(extra_list)}")
    
    if morae_errors["incorrect_morae"]:
        incorrect_list = [f"'{error['mora']}' instead of '{error['expected']}'" 
                         for error in morae_errors["incorrect_morae"]]
        feedback_parts.append(f"Incorrect morae: {', '.join(incorrect_list)}")
    
    if not feedback_parts:
        return "Perfect morae pronunciation!"
    
    return " | ".join(feedback_parts)

def normalize_japanese_text(text: str) -> str:
    """
    Normalize Japanese text for better morae comparison.
    Converts katakana to hiragana and handles common variations.
    """
    # Convert katakana to hiragana
    katakana_to_hiragana = {
        'ァ': 'ぁ', 'ア': 'あ', 'ィ': 'い', 'イ': 'い', 'ゥ': 'う', 'ウ': 'う',
        'ェ': 'え', 'エ': 'え', 'ォ': 'お', 'オ': 'お', 'カ': 'か', 'ガ': 'が',
        'キ': 'き', 'ギ': 'ぎ', 'ク': 'く', 'グ': 'ぐ', 'ケ': 'け', 'ゲ': 'げ',
        'コ': 'こ', 'ゴ': 'ご', 'サ': 'さ', 'ザ': 'ざ', 'シ': 'し', 'ジ': 'じ',
        'ス': 'す', 'ズ': 'ず', 'セ': 'せ', 'ゼ': 'ぜ', 'ソ': 'そ', 'ゾ': 'ぞ',
        'タ': 'た', 'ダ': 'だ', 'チ': 'ち', 'ヂ': 'ぢ', 'ッ': 'っ', 'ツ': 'つ',
        'ヅ': 'づ', 'テ': 'て', 'デ': 'で', 'ト': 'と', 'ド': 'ど', 'ナ': 'な',
        'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の', 'ハ': 'は', 'バ': 'ば',
        'パ': 'ぱ', 'ヒ': 'ひ', 'ビ': 'び', 'ピ': 'ぴ', 'フ': 'ふ', 'ブ': 'ぶ',
        'プ': 'ぷ', 'ヘ': 'へ', 'ベ': 'べ', 'ペ': 'ぺ', 'ホ': 'ほ', 'ボ': 'ぼ',
        'ポ': 'ぽ', 'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も',
        'ャ': 'ゃ', 'ヤ': 'や', 'ュ': 'ゅ', 'ユ': 'ゆ', 'ョ': 'ょ', 'ヨ': 'よ',
        'ラ': 'ら', 'リ': 'り', 'ル': 'る', 'レ': 'れ', 'ロ': 'ろ', 'ワ': 'わ',
        'ヲ': 'を', 'ン': 'ん'
    }
    
    normalized = text
    for katakana, hiragana in katakana_to_hiragana.items():
        normalized = normalized.replace(katakana, hiragana)
    
    return normalized