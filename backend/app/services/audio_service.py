import uuid
import shutil
import subprocess
from pathlib import Path
from fastapi import UploadFile

# Define output directory
TMP_AUDIO_DIR = Path("app/assets/tmp_audio")
TMP_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def _generate_filename(suffix: str) -> str:
    """Generate a unique filename for the uploaded file"""
    return f"{uuid.uuid4()}.{suffix}"

async def _save_upload_file(upload_file: UploadFile, destination: Path):
    """Save the uploaded file to the temporary directory"""
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

async def prepare_audio(upload_file: UploadFile) -> str:
    """
    Save uploaded audio and convert to mono 16kHz WAV format.
    Returns the path to the converted WAV file.
    """
    input_suffix = upload_file.filename.split(".")[-1]
    raw_filename = _generate_filename(input_suffix)
    wav_filename = _generate_filename("wav")

    raw_path = TMP_AUDIO_DIR / raw_filename
    wav_path = TMP_AUDIO_DIR / wav_filename

    # Save the uploaded file
    await _save_upload_file(upload_file, raw_path)

    # Convert to mono, 16kHz WAV
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_path),
        "-ac", "1",         # mono
        "-ar", "16000",     # 16kHz
        str(wav_path)
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Audio conversion failed: {e.stderr.decode()}") from e
    finally:
        # Cleanup raw input
        raw_path.unlink(missing_ok=True)

    return str(wav_path)