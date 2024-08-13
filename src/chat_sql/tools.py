from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from chat_sql.utils import db_conn


def run_db_query(sql_query):
    # function to return result in dict form
    return db_conn.run(sql_query, fetch="cursor").mappings().all()


# pydantic class to define function schema
class RunSQLSchema(BaseModel):
    sql_query: str = Field(description="SQL query string")
    database: str = Field(
        description="database type. This field is optional", default="postgresql"
    )


"""
RunSQLSchema and docstring of run_sql are used to define function(e.g. openAI json)
"""


@tool(args_schema=RunSQLSchema)
def run_sql(sql_query: str, database: str = "postgresql") -> str:
    """
    Run the SQL query over the database and return JSON result.
    """
    return str(run_db_query(sql_query=sql_query))


# pydantic class to define function schema
class PlotFigSchema(BaseModel):
    code: str = Field(
        description="""
    It is python(matplotlib) code. when executed, returns figure object.
    
    `Code` doesn't have any import statements. For e.g.
    It should just be a definition.
    code = "
        def plot():\n
            arr = np.random.normal(1, 1, size=100)
            fig, ax = plt.subplots()
            ax.hist(arr, bins=20)
            return fig
    "
    """
    )


@tool(args_schema=PlotFigSchema)
def plot_fig(code: str):
    """
    A function to plot chart or figure.
    """
    fig = None
    try:
        exec_locals = {}  # hook to store variables
        exec(code, globals(), exec_locals)
        fig = exec_locals["plot"]()  # access plot function defined inside exec
    except SyntaxError as e:
        return f"SyntaxError in the code\n{str(e)}", fig
    except Exception as e:
        return str(e), fig

    return "This function has drawn a plot for you.", fig
