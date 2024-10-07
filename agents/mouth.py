from typing import Iterable, override

from pandas import array

from agents.Agent import Agent
from agents.prompts import MOUTH_SYSTEM_PROMPT, MOUTH_USER_PROMPT
from resources import openai, tone_data
from utils import calculate_similarity, get_embedding


class MouthAgent(Agent):

    def __init__(
        self,
        model: str,
        debug: bool = False
    ) -> None:

        super().__init__(type='MouthAgent')

        self.debug = debug
        self.model = model

    def get_example(self, user_message, assistant_message) -> Iterable[str]:
        top_user_examples = sorted(tone_data, key=lambda x: calculate_similarity(get_embedding(user_message), x['user_embedding']), reverse=True)[:5]
        top_bad_reply_examples = sorted(tone_data, key=lambda x: calculate_similarity(get_embedding(assistant_message), x['bad_reply_embedding']), reverse=True)[:5]
        concat_examples = top_user_examples + top_bad_reply_examples
        examples = set([f'user: {data['user']}\nbad_reply: {data['bad_reply']}\ngood_reply: {data['good_reply']}' for data in concat_examples])
        return examples

    @override
    def run(self, user_input) -> str | None:
        user_message = user_input["user"]
        assistant_message = user_input["assistant"]
        content = f'user: {user_message}\nassistant: {assistant_message}'
        examples = self.get_example(user_message=user_message, assistant_message=assistant_message)
        prompt = str.format(MOUTH_USER_PROMPT, content=content, examples=examples)
        if self.debug: print(f'submit mouth prompt: {prompt}')
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                { "role": "system", "content": MOUTH_SYSTEM_PROMPT },
                { "role": "user", "content": prompt }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content


    @override
    def run_stream(self, user_input) -> Iterable[str]:
        user_message = user_input["user"]
        assistant_message = user_input["assistant"]
        content = f'user: {user_message}\nassistant: {assistant_message}'
        examples = self.get_example(user_message=user_message, assistant_message=assistant_message)
        prompt = str.format(MOUTH_USER_PROMPT, content=content, examples=examples)
        if self.debug: print(f'submit mouth prompt: {prompt}')
        stream = openai.chat.completions.create(
            model=self.model,
            messages=[
                { "role": "system", "content": MOUTH_SYSTEM_PROMPT },
                { "role": "user", "content": prompt }
            ],
            temperature=0.7,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                if self.debug: print(f'got: {chunk.choices[0].delta.content}')
                yield chunk.choices[0].delta.content
