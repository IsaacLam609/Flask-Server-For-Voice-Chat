# Flask Server for Voice Chat with Humanoid

## Introduction
This project focuses on developing a flask server which receives end user's audio message 
sent from a humanoid robot (or other devices), converts it to text (speech recognition), generates a text response 
(using natural language processing) and plays the synthesized audio response (speech synthesis).
It is also integrated with the Home Assistant platform to control smart home devices by sending MQTT messages.

## Usage
- In settings.py, choose
  - the speech to text service you wish to use - Whisper (local) or Azure (cloud)
  - the OpenAI service you wish to use - Home Assistant (text generation and smart device control) or Azure (text generation only)
- Start the flask server by running main.py.
- Send the audio file to the flask server from the client.
- Wait for the audio response to be played.

## Architecture
- **Components:**
  - **Humanoid Robot** (or other clients): The robot which records user's speech.
  - **Home Assistant**: The platform for managing smart home devices.
  - **Speech Service**: The middleware facilitating the communication.
- **Flow:**
  1. Flask server receives the audio file.
  2. Speech recognition: the flask server process the audio locally using OpenAI Whisper or sends the audio to Azure and gets the recognized text message.
  3. Natural language processing: the flask server sends the recognized text to Azure or Home Assistant and gets the text response.
  4. Speech synthesis: the flask server sends the text response to Azure and plays the synthesized audio response.

## Acknowledgements
- [Azure Speech Service documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [Azure OpenAI Service documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [OpenAI Whisper repository](https://github.com/openai/whisper)
- [Flask documentation](https://flask.palletsprojects.com/en/3.0.x/)
- [Home Assistant documentation](https://www.home-assistant.io/docs/)