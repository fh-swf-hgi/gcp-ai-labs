import urllib.request
from pathlib import Path

from google.cloud import speech


DATASET_URL = (
    "https://raw.githubusercontent.com/fhswf/datasets/main/audio/TransrapidAusschnitt.wav"
)
audio_file = Path("TransrapidAusschnitt.wav")


def ensure_audio_file(path):
    if path.exists():
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(DATASET_URL, path)


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
    local_audio_file = Path(__file__).parent / audio_file
    ensure_audio_file(local_audio_file)
    transcribe_file(local_audio_file)
