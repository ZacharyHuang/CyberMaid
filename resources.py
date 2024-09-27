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
