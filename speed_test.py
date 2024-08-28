import time
import whisper
import home_assistant_openai
import azure_stt_tts


def speech_to_speech_test():
    # speech to text
    stt_start_time = time.time()
    text = azure_stt_tts.azure_speech_to_text()
    stt_end_time = time.time()
    stt_time = stt_end_time - stt_start_time

    # OpenAI
    openai_start_time = time.time()
    response = home_assistant_openai.generate_response(text)
    openai_end_time = time.time()
    openai_time = openai_end_time - openai_start_time

    # text to speech
    tts_start_time = time.time()

    azure_stt_tts.azure_text_to_speech(response)

    tts_end_time = time.time()
    tts_time = tts_end_time - tts_start_time

    print("stt:", stt_time, "openai:", openai_time, "tts:", tts_time)
    print("total:", stt_time+openai_time+tts_time)


speech_to_speech_test()
