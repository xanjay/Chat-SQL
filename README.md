# Chat SQL

An application to chat with your database.

Ask question in natural language and the underlying LLM model can answer aything from your database.

It can write SQL query, connect to your database and run the query for you.

![UI](/docs/img/app_ui.png)
## Tools Used:
- Langchain - LLM framework
- OpenAI - LLM model
- Streamlit - web app
- Postgres - database

Note: This app is tested in OpenAI+postgres, but can be adapted to other model/db with minimal changes.

## Usage

Install poetry and dependencies:
```bash
pipx install poetry && poetry install
```
Run app
```bash
streamlit run src/chat_sql/app.py
```
