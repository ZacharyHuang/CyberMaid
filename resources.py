import json
import os

from openai import AzureOpenAI

def create_openai() -> AzureOpenAI:

    key = os.getenv('AZURE_OPENAI_API_KEY', None)
    if not key:
        raise KeyError('AZURE_OPENAI_API_KEY not found in environment variables')
    
    return AzureOpenAI(
        azure_endpoint='https://eastus.api.cognitive.microsoft.com/',
        api_key=key,
        api_version='2024-05-01-preview'
    )

openai = create_openai()

def get_weather_api_key() -> str:
    key = os.getenv('WEATHER_API_KEY', None)
    if not key:
        raise KeyError('WEATHER_API_KEY not found in environment variables')
    
    return key

weather_api_key = get_weather_api_key()

def get_tone_data():
    data = []
    with open('tone.jsonl', encoding='utf-8') as tone_file:
        for line in tone_file:
            data.append(json.loads(line))

    return data

tone_data = get_tone_data()