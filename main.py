import json
from typing import Iterable
import streamlit as st
import agents

def main():

    init_state()

    show_context()

    if user_input := st.chat_input('哼，主人又要麻烦我了吗？快说吧，谁让我是你的女仆呢？'):
        show_user_message(user_input)
        with st.chat_message('assistant'):
            msg_container = st.empty()
            msg_container.markdown('...')
            brain_response = st.session_state.brain_agent.run(user_input=user_input)
            show_assistant_message_stream(msg_container, st.session_state.mouth_agent.run_stream({'user': user_input, 'assistant': brain_response}))

def init_state() -> None:

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'brain_agent' not in st.session_state:
        with open('config.json', encoding='utf-8') as config_file:
            config = json.load(config_file)
        st.session_state.brain_agent = agents.create_brain(config['brain_model'])
        
    if 'mouth_agent' not in st.session_state:
        with open('config.json', encoding='utf-8') as config_file:
            config = json.load(config_file)
        st.session_state.mouth_agent = agents.create_mouth(config['mouth_model'])

def show_context() -> None:

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

def show_user_message(user_input: str) -> None:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

def show_assistant_message_stream(container, assistant_input: Iterable[str]) -> None:
    words = []
    for word in assistant_input:
        words.append(word)
        container.markdown(''.join(words).strip())

    st.session_state.messages.append({'role': 'assistant', 'content': ''.join(words).strip()})

if __name__ == '__main__':
    main()
