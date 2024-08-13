import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
import azure_key

PLAY_AUDIO = False      # whether to play the audio file locally on this device (for development only)


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
    Removes the specified unwanted characters from the input string to exclude them in text to speech conversion.

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
    speech_config = speechsdk.SpeechConfig(subscription=azure_key.SUBSCRIPTION_KEY, region=azure_key.REGION)
    speech_config.speech_recognition_language = "zh-HK"

    audio_config = speechsdk.audio.AudioConfig(filename="user_audio.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    print("Azure speech to text finished")

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


# stt_result = azure_speech_to_text()
# tts_text = ("梗係無問題啦！介紹三本書俾你："
#             "1. **《小王子》**：呢本係法國作家安東尼·德·聖-埃克蘇佩里寫嘅一本經典童話書。講述咗一個小王子嘅故事，佢喺唔同嘅星球之間旅行，見識咗唔同嘅人同事物，最終明白咗愛與友誼嘅真諦。"
#             "2. **《紅樓夢》**：由清代作家曹雪芹所寫，呢本小說描繪咗賈府大家族嘅興衰，幾百個人物角色錯綜複雜嘅關係同命運，係中國古代文學嘅四大名著之一。"
#             "3. **《追風箏的孩子》**：由阿富汗裔美國作家卡勒德·胡賽尼所寫，呢本小說講述咗兩個阿富汗男孩嘅故事，佢哋喺戰亂中成長，面對友情、背叛同救贖嘅困惑。"
#             "呢三本書風格各異，但每一本都好值得一睇。你有興趣睇邊本？")
# cleaned = remove_unwanted_chars(tts_text)
# azure_text_to_speech(tts_text)
