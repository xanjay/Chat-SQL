from langchain_core.messages import AIMessage, HumanMessage
from chat_sql.utils import db_conn
from chat_sql.main import get_model

def test_postgres_connection():
    res = db_conn.run("select 1")
    assert res == str([(1,)])

def test_ai_model():
    model = get_model()
    msg = model.invoke([HumanMessage("Hi")])
    
    assert type(msg)==AIMessage