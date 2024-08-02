import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream

speech_config = speechsdk.SpeechConfig(subscription="7ca6e78f621043fbaebf0b68fb50bbfa", region="eastus")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_config.speech_synthesis_voice_name = 'zh-HK-HiuMaanNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

text = "收到啦"

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


# Save the audio to a file
audio_data_stream = AudioDataStream(speech_synthesis_result)
audio_data_stream.save_to_wav_file("tts_output.wav")