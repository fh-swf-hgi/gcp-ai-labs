import os
import subprocess
import urllib.request
from pathlib import Path

from google.cloud import speech


DATASET_URL = (
    "https://raw.githubusercontent.com/fhswf/datasets/main/audio/Transrapid.mp3"
)
audio_file = Path("audio/Transrapid.mp3")
clip_file = Path("transrapid_clip.wav")
clip_start = 4
clip_end = 55


def ensure_audio_file(path):
    if path.exists():
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(DATASET_URL, path)


def create_wav_clip(mp3_file, wav_file, start, end):
    if wav_file.exists():
        print(f"Using existing file: {wav_file}")
        return

    duration = end - start
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start),
        "-t",
        str(duration),
        "-i",
        str(mp3_file),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-sample_fmt",
        "s16",
        str(wav_file),
    ]
    subprocess.run(cmd, check=True)


def transcribe_file(speech_file):
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio:
        content = audio.read()

    response = client.recognize(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="de-DE",
        ),
        audio=speech.RecognitionAudio(content=content),
    )

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    ensure_audio_file(audio_file)
    create_wav_clip(audio_file, clip_file, clip_start, clip_end)
    transcribe_file(clip_file)
