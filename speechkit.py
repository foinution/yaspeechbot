import logging
import requests
from creds import get_iam, get_folder_id

def text_to_speech(text):
    headers = {
        'Authorization': f'Bearer {get_iam()}',
    }
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': get_folder_id(),
    }
    response = requests.post(
        'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
        headers=headers,
        data=data
    )
    if response.status_code == 200:
        return True, response.content
    else:
        return False, "При запросе в SpeechKit возникла ошибка"

def speech_to_text(data):
    params = "&".join([
        "topic=general",
        f"folderId={get_folder_id()}",
        "lang=ru-RU"
    ])
    headers = {
        'Authorization': f'Bearer {get_iam()}',
    }
    response = requests.post(
            f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=headers, 
        data=data
    )
    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")
    else:
        return False, "При запросе в SpeechKit возникла ошибка" 