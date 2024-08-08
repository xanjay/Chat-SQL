from langchain_core.messages import HumanMessage
from chat_sql.main import initialize_assistant

def test_function_call():
    # test if model opts for function calling or not
    chain, messages = initialize_assistant()
    # simulate user question
    question = "How many departments are there?"
    messages.append(HumanMessage(content=question))
    # call model
    ai_msg = chain.invoke(messages)
    # ai_msg should contain function call
    # check if there is at least one function call in the response
    assert len(ai_msg.additional_kwargs.get('tool_calls')) > 0


