import logging
import requests
from creds import get_iam, get_folder_id

def ask_gpt(text):
	headers = {
		'Authorization': f'Bearer {get_iam()}',
		'Content-Type': 'application/json'
	}
	data = {
		"modelUri": f"gpt://{get_folder_id()}/yandexgpt-lite",
		"completionOptions": {
			"stream": False,
			"temperature": 0.6,
			"maxTokens": "200"
		},
		"messages": [
			{
				"role": "user",
				"text": text
			}
		]
	}
	response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
							 headers=headers,
							 json=data)
	if response.status_code == 200:
		text = response.json()["result"]["alternatives"][0]["message"]["text"]
		return text
	else:
		raise RuntimeError(
			'Invalid response received: code: {}, message: {}'.format(
				{response.status_code}, {response.text}
			)
		)

def count_tokens(text):
	headers = {
		'Authorization': f'Bearer {get_iam()}',
		'Content-Type': 'application/json'
	}
	data = {
	   "modelUri": f"gpt://{get_folder_id()}/yandexgpt/latest",
	   "maxTokens": 200,
	   "text": text
	}
	return len(
		requests.post(
			"https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
			json=data,
			headers=headers
		).json()['tokens']
	)

def status_check(text):
	headers = {
		'Authorization': f'Bearer {get_iam()}',
		'Content-Type': 'application/json'
	}
	data = {
		"modelUri": f"gpt://{get_folder_id()}/yandexgpt-lite",
		"completionOptions": {
			"stream": False,
			"temperature": 0.6,
			"maxTokens": "200"
		},
		"messages": [
			{
				"role": "user",
				"text": text
			}
		]
	}
	response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
							 headers=headers,
							 json=data)
	text = response.status_code
	return text