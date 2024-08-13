from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from chat_sql.tools import run_sql, run_db_query, plot_fig
from langchain_core.messages import SystemMessage, AIMessage

from dotenv import dotenv_values

config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]
OPENAI_MODEL = config["OPENAI_MODEL"]

AVAILABLE_TOOLS = {"run_sql": run_sql, "plot_fig": plot_fig}


def get_model():
    # initialize openai llm
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        max_retries=2,
        api_key=OPENAI_API_KEY,
    )
    # add function call
    llm_with_tools = llm.bind_tools(list(AVAILABLE_TOOLS.values()))
    return llm_with_tools


def get_db_schema():
    schema = run_db_query("""
                  SELECT table_name, column_name, data_type
                  FROM information_schema.columns
                  WHERE table_schema = 'public'
                  ORDER BY table_name, ordinal_position;""")
    return schema


def make_tool_calls(ai_tool_calls):
    plots = []
    tool_messages = []

    for tool_call in ai_tool_calls:
        selected_tool = AVAILABLE_TOOLS[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])

        # this tool returns artifacts along with message
        if tool_call["name"] == "plot_fig":
            tool_message = ToolMessage(
                content=tool_output[0], tool_call_id=tool_call["id"]
            )
            plots.append(tool_output[-1])
        else:
            tool_message = ToolMessage(
                content=tool_output, tool_call_id=tool_call["id"]
            )
        tool_messages.append(tool_message)
    return tool_messages, plots


def run_model(messages, model, artifacts=None):
    # call model
    ai_msg = model.invoke(messages)
    if artifacts:
        # recreate AI message with added plots
        ai_msg = AIMessage(ai_msg.content, plots=artifacts)

    messages.append(ai_msg)
    # make tool calls (if any)
    if len(ai_tool_calls := ai_msg.tool_calls):
        tool_messages, plots = make_tool_calls(ai_tool_calls)
        return run_model(messages + tool_messages, model, artifacts=plots)

    return messages


def initialize_assistant():
    messages = []
    system_message = """
        You are a database expert.
        You need to answer database related answer along with normal conversation.
        If you feel like you need to access database, follow below steps:
        1. Convert the user question into SQL query
        2. Validate the query with the schema
        3. Run the query

        Notes:
        - If you need to run query, only run SELECT query.

        Database schema is as follows:
        {db_schema}
    """

    messages.append(
        SystemMessage(content=system_message.format(**{"db_schema": get_db_schema()}))
    )  # noqa: E501

    # model init call
    chain = get_model()
    ai_msg = chain.invoke(messages)
    messages.append(ai_msg)
    return chain, messages
