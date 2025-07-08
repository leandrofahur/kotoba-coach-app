import whisper

model = whisper.load_model("small")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes the given audio file using Whisper, specifying Japanese.
    Returns the raw transcription text, but only if it contains Japanese characters.
    """
    result = model.transcribe(audio_path, language="ja")
    text = result["text"].strip()
    # Only keep if contains Japanese (hiragana, katakana, kanji)
    import re
    if not re.search(r"[\u3040-\u30ff\u4e00-\u9faf]", text):
        return ""  # Or return a special message if preferred
    return text



