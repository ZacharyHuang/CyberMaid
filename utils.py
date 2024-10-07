import json

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from resources import openai, tone_data

def get_embedding(text: str) -> list[float]:
    return openai.embeddings.create(input=text, model='text-embedding-3-small').data[0].embedding

def calculate_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    array1 = np.array(embedding1).reshape(1, -1)
    array2 = np.array(embedding2).reshape(1, -1)
    return cosine_similarity(array1, array2)[0][0]

def update_tone_data(data) -> None:
    
    data['user_embedding'] = get_embedding(data['user'])
    data['bad_reply_embedding'] = get_embedding(data['bad_reply'])

    with open('tone.jsonl', 'a', encoding='utf-8') as tone_file:
        tone_file.write(json.dumps(data, ensure_ascii=False) + '\n')
        
    tone_data.append(data)