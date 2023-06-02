from pytube import YouTube
from moviepy.editor import *
import os

#source: https://pytube.io/en/latest/user/quickstart.html#downloading-a-video
def downloadYouTube(videourl, path):

    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
    yt.default_filename
    name = yt.default_filename.replace(" ","_")
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isfile(os.path.join(path, name)):
        yt.download(path, filename=name)
    return os.path.join(path, name)

#source https://www.askpython.com/python/examples/extract-audio-from-video
def mp4_to_wav(mp4file,wavfile, sfrom, sto):
    if not os.path.isfile(wavfile):
        videoclip=VideoFileClip(mp4file)
        audioclip=videoclip.audio
        audioclip = audioclip.subclip(sfrom,sto)
        audioclip.write_audiofile(wavfile, codec='pcm_s16le', ffmpeg_params=["-ac", "1"])
        audioclip.close()
        videoclip.close()
    else:
        print("File already exists!")

#source: https://cloud.google.com/speech-to-text/docs/sync-recognize
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
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

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")


url = "https://www.youtube.com/watch?v=3dWkS84uxPU"
name = downloadYouTube(url, ".")
audioname = os.path.splitext(name)[0] + ".wav"
mp4_to_wav(name,audioname, 4, 49)
transcribe_file(audioname)
