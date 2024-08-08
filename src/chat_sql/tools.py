from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from chat_sql.utils import db_conn

def run_db_query(sql_query):
    # function to return result in dict form
    return db_conn.run(sql_query, fetch="cursor").mappings().all()

# pydantic class to define function schema
class RunSQLSchema(BaseModel):
    sql_query: str = Field(description="SQL query string")
    database : str = Field(description="database type. This field is optional. default value: `postgresql`")  # noqa: E501


"""
RunSQLSchema and docstring of run_sql are used to define function(e.g. openAI json)
"""
@tool(args_schema=RunSQLSchema)
def run_sql(sql_query: str, database: str = "postgresql") -> str:
    """Run the SQL query over the database and return JSON result"""
    return str(run_db_query(sql_query=sql_query))

