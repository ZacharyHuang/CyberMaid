from abc import ABC, abstractmethod
import json
from typing import Iterator

from openai import NotGiven, NOT_GIVEN

from resources import openai

class Agent(ABC):

    def __init__(self, type: str, name: str) -> None:
        self.type = type
        self.name = name
        
    @abstractmethod
    def run(self, user_input: str, instructions: str | NotGiven | None = NOT_GIVEN) -> str:
        pass

    @abstractmethod
    def run_stream(self, user_input: str, instructions: str | NotGiven | None = NOT_GIVEN) -> Iterator[str]:
        pass

class AgentFactory:

    @staticmethod
    def create(type: str, debug: bool = False) -> Agent:

        with open('agents.json', 'r') as config:
            agents = json.load(config)

        if type not in agents:
            raise KeyError(f'{type} is not defined in agents.json')
        
        agent = agents[type]
        if (type == 'Maid'):
            return Assistant(
                type=type,
                name = agent['name'],
                instructions=agent['instructions'],
                model=agent['model'],
                debug=debug
            )
        else:
            raise NotImplementedError(f'{type} agent is not supported yet')

class Assistant(Agent):

    def __init__(self, type: str, name: str, instructions: str, model: str, debug: bool = False) -> None:
        super().__init__(
            type=type,
            name=name
        )

        self.debug = debug
        self.thread = openai.beta.threads.create()
        self.assistant = openai.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )


    def run(self, user_input: str, instructions: str | NotGiven | None = NOT_GIVEN) -> str | None:
        openai.beta.threads.messages.create(
            thread_id=self.thread.id,
            role='user',
            content=user_input
        )

        run = openai.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )

        if self.debug: print(run.status)
        if run.status == 'completed':
            msg = openai.beta.threads.messages.list(thread_id=self.thread.id)[-1]
            if self.debug: print(msg)
            return msg
        else:
            return None


    def run_stream(self, user_input: str, instructions: str | NotGiven | None = NOT_GIVEN) -> Iterator[str]:
        openai.beta.threads.messages.create(
            thread_id=self.thread.id,
            role='user',
            content=user_input
        )
        
        with openai.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                instructions=instructions
            ) as stream:
                for event in stream:
                    if event.data.object == 'thread.message.delta':
                        for content in event.data.delta.content:
                            if content.type == 'text':
                                yield content.text.value
                    else:
                        if self.debug: print(event)
