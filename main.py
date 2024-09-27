import os
from openai import AzureOpenAI
import streamlit as st

def main():

    if 'client' not in st.session_state:
        key = os.getenv('AZURE_OPENAI_API_KEY', None)
        endpoint = 'https://eastus.api.cognitive.microsoft.com/'
        name = 'May'
        instructions = 'You are a cyber maid named May, you serve user as a maid in computer.'
        model = 'gpt-4o-mini'

        st.session_state.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=key,
            api_version='2024-05-01-preview'
        )
        
        st.session_state.assistant = st.session_state.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )
        
        st.session_state.thread = st.session_state.client.beta.threads.create()

        
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if user_input := st.chat_input('Master, May is at your service.'):
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        with st.chat_message('user'):
            st.markdown(user_input)


        st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role='user',
            content=user_input
        )

        with st.chat_message('assistant'):
            box = st.empty()
            words = []
            with st.session_state.client.beta.threads.runs.stream(
                thread_id=st.session_state.thread.id,
                assistant_id=st.session_state.assistant.id,
                instructions='Please answer starting with "Master, "'
            ) as stream:
                for event in stream:
                    if event.data.object == 'thread.message.delta':
                        for content in event.data.delta.content:
                            if content.type == 'text':
                                words.append(content.text.value)
                                box.markdown(f'{''.join(words).strip()}')
                st.session_state.messages.append({'role': 'assistant', 'content': ''.join(words).strip()})

if __name__ == '__main__':
    main()import os
from openai import AzureOpenAI
import streamlit as st

def main():

    if 'client' not in st.session_state:
        key = os.getenv('AZURE_OPENAI_API_KEY', None)
        endpoint = 'https://eastus.api.cognitive.microsoft.com/'
        name = 'May'
        instructions = 'You are a cyber maid named May, you serve user as a maid in computer.'
        model = 'gpt-4o-mini'

        st.session_state.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=key,
            api_version='2024-05-01-preview'
        )
        
        st.session_state.assistant = st.session_state.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )
        
        st.session_state.thread = st.session_state.client.beta.threads.create()

        
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if user_input := st.chat_input('Master, May is at your service.'):
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        with st.chat_message('user'):
            st.markdown(user_input)


        st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role='user',
            content=user_input
        )

        with st.chat_message('assistant'):
            box = st.empty()
            words = []
            with st.session_state.client.beta.threads.runs.stream(
                thread_id=st.session_state.thread.id,
                assistant_id=st.session_state.assistant.id,
                instructions='Please answer starting with "Master, "'
            ) as stream:
                for event in stream:
                    if event.data.object == 'thread.message.delta':
                        for content in event.data.delta.content:
                            if content.type == 'text':
                                words.append(content.text.value)
                                box.markdown(f'{''.join(words).strip()}')
                st.session_state.messages.append({'role': 'assistant', 'content': ''.join(words).strip()})

if __name__ == '__main__':
    main()