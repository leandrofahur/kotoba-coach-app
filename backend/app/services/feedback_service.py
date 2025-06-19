from Levenshtein import distance

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


