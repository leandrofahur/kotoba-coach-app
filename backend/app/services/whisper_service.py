import whisper

model = whisper.load_model("small")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes the given audio file using Whisper, specifying Japanese.
    Returns the raw transcription text.
    """
    result = model.transcribe(audio_path, language="japanese")
    return result["text"].strip()



