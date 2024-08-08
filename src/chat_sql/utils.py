from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import dotenv_values

# database connection
config = dotenv_values(".env")

POSTGRES_USER = config["POSTGRES_USER"]
POSTGRES_PASSWORD = config["POSTGRES_PASSWORD"]
POSTGRESS_URL = config["POSTGRESS_URL"]
POSTGRESS_DB = config["POSTGRESS_DB"]

db_conn = SQLDatabase.from_uri(f"""postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRESS_URL}/{POSTGRESS_DB}""")
