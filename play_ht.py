import time
from pyht import Client, TTSOptions, Format

# Play HT is an alternative for text to speech services

# initialize the Play.ht client with your credentials
client = Client("your-id", "your-key")

# configure the TTS options
options = TTSOptions(
    voice="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
    sample_rate=8000,
    format=Format.FORMAT_MP3,
    speed=1,
)

# the text you want to convert to speech
text = "Hello, this is a test of the text-to-speech functionality."

tts_start = time.time()
# generate the audio and save it to a file
with open("play_ht_output.mp3", "wb") as f:
    for chunk in client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
        f.write(chunk)

tts_end = time.time()
print(tts_end-tts_start)

print("Audio file saved")
