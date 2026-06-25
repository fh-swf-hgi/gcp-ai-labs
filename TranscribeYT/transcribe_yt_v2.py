import sys

from google.cloud import speech


def transcribe_gcs(gcs_uri):
    client = speech.SpeechClient()

    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            language_code="de-DE",
            enable_automatic_punctuation=True,
        ),
        audio=speech.RecognitionAudio(uri=gcs_uri),
    )

    print("Waiting for Speech-to-Text operation to finish...")
    response = operation.result(timeout=600)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].startswith("gs://"):
        print("Usage: python transcribe_yt_v2.py gs://BUCKET/Transrapid.mp3")
        sys.exit(1)

    transcribe_gcs(sys.argv[1])
