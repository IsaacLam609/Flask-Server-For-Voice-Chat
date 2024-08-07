from flask import Flask, request
import whisper
import mqtt_methods
import azure_stt_tts

# SPEECH_TO_TEXT_SERVICE = "Whisper"
SPEECH_TO_TEXT_SERVICE = "Azure"

app = Flask(__name__)

if SPEECH_TO_TEXT_SERVICE == "Whisper":                                # OpenAI Whisper speech to text model
    stt_model = whisper.load_model("large-v3", device="cuda")    # use cpu for the 'device' argument if no gpu available

@app.route('/upload', methods=['POST'])
def speech_to_text():

    with open("user_audio.wav", 'wb') as f:
        f.write(request.data)

    if SPEECH_TO_TEXT_SERVICE == "Whisper":                             # OpenAI Whisper speech to text
        print("Start Whisper speech to text")
        print(f"Model is using device: {next(stt_model.parameters()).device}")
        result = stt_model.transcribe(audio="user_audio.wav", language="yue")
        text = result["text"]
        print(text)
    elif SPEECH_TO_TEXT_SERVICE == "Azure":
        text = azure_stt_tts.azure_speech_to_text()                     # Azure speech to text
    else:
        text = "Speech to text service not selected"
        print(text)

    # send mqtt message
    if (text == " 我想開燈") or (text == "我想開燈。"):
        mqtt_methods.mqtt_publish("/airlab/light/W402e", "On")
    elif (text == " 我想熄燈") or (text == "我想熄燈。"):
        mqtt_methods.mqtt_publish("/airlab/light/W402e", "Off")

    return "File uploaded successfully", 200


if __name__ == '__main__':
    app.run("0.0.0.0")