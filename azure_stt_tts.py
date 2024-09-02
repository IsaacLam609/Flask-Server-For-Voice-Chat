import time

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
import azure_key

PLAY_AUDIO = False      # whether to play the audio file locally on this device (for development purpose)


def azure_text_to_speech(text):
    """
    Synthesize the speech audio file from the input text using Azure AI services.

    Args:
        text (str): The text to be converted to speech.
    """
    print("Azure text to speech in progress")

    text = remove_unwanted_chars(text)

    speech_config = speechsdk.SpeechConfig(subscription=azure_key.SUBSCRIPTION_KEY, region=azure_key.REGION)

    if PLAY_AUDIO:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    else:
        audio_config = speechsdk.audio.AudioOutputConfig(filename="tts_output.wav")     # save the audio file

    speech_config.speech_synthesis_voice_name = 'zh-HK-HiuMaanNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    if PLAY_AUDIO:
        # Save the audio to a file
        audio_data_stream = AudioDataStream(speech_synthesis_result)
        audio_data_stream.save_to_wav_file("tts_output.wav")


def remove_unwanted_chars(input_string):
    """
    Removes unwanted characters from the input string to exclude them in speech synthesis (text to speech).

    Args:
        input_string (str): The input string to be cleaned.

    Returns:
        str: The input string with the unwanted characters removed.
    """
    unwanted_chars = "*"
    return ''.join(char for char in input_string if char not in unwanted_chars)


def azure_speech_to_text():
    """
    Transcribed the speech audio file to text using Azure AI services.

    Returns:
        str: The text transcribed from the audio file.
    """
    print("Azure speech to text started")
    speech_config = speechsdk.SpeechConfig(subscription=azure_key.SUBSCRIPTION_KEY, region=azure_key.REGION,
                                           speech_recognition_language="zh-HK")
    audio_config = speechsdk.audio.AudioConfig(filename="user_audio.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    start = time.time()
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    end = time.time()

    print("Azure speech to text finished")
    print(end-start)

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    return speech_recognition_result.text


def azure_speech_to_text_continuous():
    """Performs continuous speech recognition with input from an audio file"""

    start = time.time()

    speech_config = speechsdk.SpeechConfig(subscription=azure_key.SUBSCRIPTION_KEY, region=azure_key.REGION,
                                           speech_recognition_language="zh-HK")
    audio_config = speechsdk.audio.AudioConfig(filename="user_audio.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        # print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    # speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.1)

    speech_recognizer.stop_continuous_recognition()
    end = time.time()

    print("Azure speech to text finished")
    print(end-start)



