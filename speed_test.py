import time

import whisper

import home_assistant_openai
import azure_stt_tts


def test():
    # stt_model = whisper.load_model("large-v3", device="cuda")  # use cpu for the 'device' argument if no gpu available
    # speech to text
    stt_start_time = time.time()

    text = azure_stt_tts.azure_speech_to_text()                     # Azure speech to text
    # result = stt_model.transcribe(audio="tts_output.wav", language="yue")
    # text = result["text"]
    print(text)

    stt_end_time = time.time()
    stt_time = stt_end_time - stt_start_time

    print(stt_time)

    # # OpenAI
    # openai_start_time = time.time()
    #
    # response = home_assistant_openai.generate_response(text)
    #
    # openai_end_time = time.time()
    # openai_time = openai_end_time - openai_start_time
    #
    # # text to speech
    # tts_start_time = time.time()
    #
    # azure_stt_tts.azure_text_to_speech(response)
    #
    # tts_end_time = time.time()
    # tts_time = tts_end_time - tts_start_time
    #
    # print("stt:", stt_time, "openai:", openai_time, "tts:", tts_time)


test()
