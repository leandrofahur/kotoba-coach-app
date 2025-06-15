import torch
import whisper
import torchaudio
from scipy.spatial.distance import cosine

# Load Whisper model once
model = whisper.load_model("base")

AUDIO_PATH = "app/assets/audio/ohayogozaimasu.mp3"

def load_audio_embedding(file_path: str):
    # Load and preprocess audio
    audio, sr = torchaudio.load(file_path)
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
        audio = resampler(audio)
    audio = torch.mean(audio, dim=0)  # Convert to mono
    audio = whisper.pad_or_trim(audio.numpy())

    # Convert to mel spectrogram
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Encode with Whisper
    with torch.no_grad():
        embedding = model.encode(audio=mel)

    return embedding.squeeze().cpu().numpy()

# Load reference embedding once
REFERENCE_EMBEDDING = load_audio_embedding(AUDIO_PATH)

def score_user_audio(user_path: str) -> float:
    user_embedding = load_audio_embedding(user_path)
    similarity = 1 - cosine(user_embedding, REFERENCE_EMBEDDING)
    return round(similarity * 100, 2)
