import json

from agents.Agent import Agent
from agents.assistants import Assistant
from agents.brain import BrainAgent
from agents.mouth import MouthAgent

with open('agents/agents.json', encoding='utf-8') as config_file:
    config = json.load(config_file)

def create(profile_key, debug: bool = False) -> Agent:

    if profile_key not in config:
        raise KeyError(f'{profile_key} profile_key not found in config')


    profile = config[profile_key]
    if (profile['type'] == 'Assistant'):
        return Assistant(
            type=profile['type'],
            name = profile['name'],
            instructions=profile['instructions'],
            model=profile['model'],
            tools=profile['tools'],
            debug=debug
        )
    if (profile['type'] == 'BrainAgent'):
        return BrainAgent(
            model=profile['model'],
            debug=debug
        )
    if (profile['type'] == 'MouthAgent'):
        return MouthAgent(
            model=profile['model'],
            debug=debug
        )
    else:
        raise NotImplementedError(f'{profile['type']} agent is not supported yet')

debug_mode = True

def create_brain(model: str) -> Agent:
    return BrainAgent(
        model=model,
        debug=debug_mode
    )

def create_mouth(model: str) -> Agent:
    return MouthAgent(
        model=model,
        debug=debug_mode
    )
