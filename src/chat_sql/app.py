from main import initialize_assistant, run_model
import streamlit as st
from langchain_core.messages import HumanMessage


def display_chat_messages(chat_messages):
    for message in chat_messages:
        if message.type in ("ai", "human") and len(message.content):
            with st.chat_message(message.type):
                st.markdown(message.content)

                if hasattr(message, "plots"):
                    for plot in message.plots:
                        st.pyplot(plot)


st.title("Chat with database")

if "messages" not in st.session_state:
    st.session_state.chain, st.session_state.messages = initialize_assistant()

display_chat_messages(st.session_state.messages)

if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("human"):
        st.markdown(prompt)

    if st.session_state.chain:
        ai_messages = run_model(st.session_state.messages, st.session_state.chain)
        # take only new messages
        new_messages = ai_messages[len(st.session_state.messages) - 1 :]
        display_chat_messages(new_messages)
        st.session_state.messages = ai_messages
    else:
        st.error("Assistant not initialized. Please try again later.")
