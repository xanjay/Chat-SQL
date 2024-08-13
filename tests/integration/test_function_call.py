from langchain_core.messages import HumanMessage
from chat_sql.main import initialize_assistant, run_model
from matplotlib.figure import Figure


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
    assert len(ai_msg.additional_kwargs.get("tool_calls")) > 0


def test_plot_response():
    # test if the model returns plot when asked to plot data
    chain, messages = initialize_assistant()
    # simulate user question
    question = "Can you plot bar chart showing sample population of continents?"
    messages.append(HumanMessage(content=question))
    # call model
    ai_messages = run_model(messages, chain)
    last_msg = ai_messages[-1]  # take last msg

    assert hasattr(last_msg, "plots") is True
    plots = last_msg.plots

    assert len(plots) > 0
    for plot in plots:
        assert isinstance(plot, Figure) is True
