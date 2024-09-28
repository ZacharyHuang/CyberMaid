import streamlit as st
from agents import AgentFactory

def main():

    if 'agent' not in st.session_state:
        st.session_state.agent = AgentFactory.create('Maid', debug=True)

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if user_input := st.chat_input(f'Master, {st.session_state.agent.name} is at your service.'):
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        with st.chat_message('user'):
            st.markdown(user_input)

        with st.chat_message('assistant'):
            msg_box = st.empty()
            words = []
            for word in st.session_state.agent.run_stream(user_input=user_input):
                words.append(word)
                msg_box.markdown(''.join(words).strip())
                
            st.session_state.messages.append({'role': 'assistant', 'content': ''.join(words).strip()})

if __name__ == '__main__':
    main()
