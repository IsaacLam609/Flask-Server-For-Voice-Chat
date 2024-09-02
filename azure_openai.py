from openai import AzureOpenAI
import azure_key


def generate_response(text):
    """
    Gets a response for a given message using Azure OpenAI.

    Args:
        text (str): The input text.

    Returns:
        str: The response text.
    """
    print("Generating response...")
    client = AzureOpenAI(
      azure_endpoint=azure_key.OPENAI_ENDPOINT,
      api_key=azure_key.OPENAI_KEY,
      api_version="2024-02-01"
    )

    response = client.chat.completions.create(
        model="gpt-4o",                  # deployment name
        messages=[
            {"role": "system", "content": "你係一個獨居老人嘅智慧家居助手。你嘅主要功能係操控智慧家居嘅裝置，同埋用廣東話同老人傾計。"
                                          "係控制裝置前記得先向用家確認"},
            {"role": "user", "content": text}
        ]
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content
