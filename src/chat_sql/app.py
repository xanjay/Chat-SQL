from chat_sql.main import initialize_assistant, run_model
from langchain_core.messages import HumanMessage
import streamlit as st


st.title("Chat with database")

if "messages" not in st.session_state:
    st.session_state.chain, st.session_state.messages = initialize_assistant()

for message in st.session_state.messages:
    if message.type != "system":
        with st.chat_message(message.type):
            st.markdown(message.content)

if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("human"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.chain:
            ai_messages = run_model(
                prompt, st.session_state.messages, st.session_state.chain
            )
            st.markdown(ai_messages[-1].content)
            st.session_state.messages += ai_messages
        else:
            st.error("Assistant not initialized. Please try again later.")
