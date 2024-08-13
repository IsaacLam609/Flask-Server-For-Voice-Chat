import time

from flask import Flask, request
import whisper

import home_assistant_openai
import mqtt_methods
import azure_stt_tts
import azure_openai
import settings

app = Flask(__name__)

if settings.SPEECH_TO_TEXT_SERVICE == "Whisper":                                # OpenAI Whisper speech to text model
    stt_model = whisper.load_model("large-v3", device="cuda")    # use cpu for the 'device' argument if no gpu available


@app.route('/upload', methods=['POST'])
def speech_to_speech():       # CHANGE THIS METHOD NAME

    with open("user_audio.wav", 'wb') as f:
        f.write(request.data)

    # speech to text
    if settings.SPEECH_TO_TEXT_SERVICE == "Whisper":                    # OpenAI Whisper speech to text
        print("Start Whisper speech to text")
        print(f"Model is using device: {next(stt_model.parameters()).device}")
        result = stt_model.transcribe(audio="user_audio.wav", language="yue")
        text = result["text"]
        print(text)
    elif settings.SPEECH_TO_TEXT_SERVICE == "Azure":
        text = azure_stt_tts.azure_speech_to_text()                     # Azure speech to text
    else:
        text = "Speech to text service not selected"
        print(text)

    # OpenAI
    if settings.OPENAI_SERVICE == "Azure":
        response = azure_openai.generate_response(text)
    elif settings.OPENAI_SERVICE == "Home Assistant":
        response = home_assistant_openai.generate_response(text)
    else:
        response = "OpenAI service not selected"
        print(response)

    # text to speech
    azure_stt_tts.azure_text_to_speech(response)

    return "File uploaded successfully", 200


if __name__ == '__main__':
    app.run("0.0.0.0")
