from typing import Iterable, override

from openai.types.beta.assistant_tool_param import AssistantToolParam

from agents.Agent import Agent
from resources import openai
import tools


class Assistant(Agent):

    def __init__(
        self,
        type: str,
        name: str,
        instructions: str,
        model: str,
        tools: Iterable[AssistantToolParam],
        debug: bool = False
    ) -> None:

        super().__init__(type=type)

        self.debug = debug
        self.thread = openai.beta.threads.create()
        self.assistant = openai.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=tools
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
                if self.debug: print(f'call tool: {tool_call.function.name}')
                tool_output = tools.process_tool_call(tool_call)
                tool_outputs.append(tool_output)
                if self.debug: print(f'tool {tool_call.function.name} output: {tool_output}')

            run = openai.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=self.thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        if run.status == 'completed':
            message = openai.beta.threads.messages.list(thread_id=self.thread.id).data[-1].content[0].text
            if self.debug: print(f'final message: {message}')
            return message


    @override
    def run_stream(self, user_input) -> Iterable[str]:
        return self.run(user_input=user_input).split()
