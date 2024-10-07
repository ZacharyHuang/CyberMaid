from typing import Iterable, override

from agents.Agent import Agent
from agents.prompts import BRAIN_PROMPT
from resources import openai
import tools


class BrainAgent(Agent):

    def __init__(
        self,
        model: str,
        debug: bool = False
    ) -> None:

        super().__init__(type='BrainAgent')

        self.debug = debug
        self.thread = openai.beta.threads.create()
        self.assistant = openai.beta.assistants.create(
            name='May',
            instructions=BRAIN_PROMPT,
            model=model,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_master_profile",
                        "description": "Get the profile of your master, including language, region, location",
                        "parameters": {}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_time",
                        "description": "Get current time",
                        "parameters": {}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get the weather in location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string", "description": "The city name in English, for example Beijing"},
                                "days": {"type": "string", "description": "how many days of forecast you are reqeusting, for example 5"}
                            },
                            "required": ["location", "days"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "record_refinement",
                        "description": "Record the response refinement per user's feedback",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user": {"type": "string", "description": "The user's original message"},
                                "bad_reply": {"type": "string", "description": "The original assistant reply that user dislikes"},
                                "good_reply": {"type": "string", "description": "The refined reply per user's feedback"}
                            },
                            "required": ["user", "bad_reply", "good_reply"]
                        }
                    }
                }
            ],
            temperature=0.7
        )

    @override
    def run(self, user_input) -> str | None:

        openai.beta.threads.messages.create(
            thread_id=self.thread.id,
            role='user',
            content=user_input
        )
        
        if self.debug: print(f'submit request: {user_input}')
        run = openai.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        
        while run.status == 'requires_action':
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                if self.debug: print(f'call tool: {tool_call.function.name} with args: {tool_call.function.arguments}')
                tool_output = tools.process_tool_call(tool_call)
                tool_outputs.append(tool_output)
                if self.debug: print(f'tool {tool_call.function.name} output: {tool_output}')

            run = openai.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=self.thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        if run.status == 'completed':
            message = openai.beta.threads.messages.list(thread_id=self.thread.id).data[0].content[0].text.value
            if self.debug: print(f'final message: {message}')
            return message
        else:
            if self.debug: print(f'unexpected run.status: {run.status}')

    @override
    def run_stream(self, user_input) -> Iterable[str]:
        return self.run(user_input=user_input).split()
