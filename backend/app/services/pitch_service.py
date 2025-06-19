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

def extract_pitch_librosa(audio_path: str, sr: int = 16000) -> list[float]:
    """
    Extract pitch (F0 in Hz) using librosa's pyin algorithm.
    Returns a list of float pitch values (0.0 where unvoiced).
    """
    y, sr = librosa.load(audio_path, sr=sr)

    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=sr
    )

    # Replace NaNs (unvoiced) with 0.0
    pitch_values = [float(p) if p is not None else 0.0 for p in f0]

    return pitch_values
