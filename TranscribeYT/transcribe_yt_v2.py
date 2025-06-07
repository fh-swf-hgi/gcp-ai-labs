import subprocess
from moviepy.editor import *
import os

def downloadYouTube(videourl, path):
    if not os.path.exists(path):
        os.makedirs(path)
    cmd = [
        "yt-dlp",
        "-f", "best[ext=mp4][vcodec!=none][acodec!=none]",
        "-o", os.path.join(path, "%(title)s.%(ext)s"),
        videourl
    ]
    subprocess.run(cmd, check=True)

    # Suche erste MP4-Datei im Zielordner
    for f in os.listdir(path):
        if f.endswith(".mp4"):
            return os.path.join(path, f)
    raise FileNotFoundError("Keine MP4-Datei gefunden.")

def mp4_to_wav(mp4file, wavfile, sfrom, sto):
    if not os.path.isfile(wavfile):
        videoclip = VideoFileClip(mp4file)
        audioclip = videoclip.audio.subclip(sfrom, sto)
        audioclip.write_audiofile(wavfile, codec='pcm_s16le', ffmpeg_params=["-ac", "1"])
        audioclip.close()
        videoclip.close()
    else:
        print("File already exists!")

def transcribe_file(speech_file):
    from google.cloud import speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="de-DE",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

# Hauptlogik
url = "https://www.youtube.com/watch?v=3dWkS84uxPU"
name = downloadYouTube(url, ".")
audioname = os.path.splitext(name)[0] + ".wav"
mp4_to_wav(name, audioname, 4, 49)
transcribe_file(audioname)
