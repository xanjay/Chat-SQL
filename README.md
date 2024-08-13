# Chat SQL

An application to chat with your database.

## Features
- Ask question in natural language and the underlying LLM model can answer anything from your database.
- It can write SQL query, connect to your database and run the query for you.
- Display visualizations/plots

![UI](/docs/img/chat_sql_ui.jpg)
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
Populate `.env` file with credentials and run the app:
```bash
streamlit run src/chat_sql/app.py
```

## Contributing
If you have any issue fixes or improvement changes. Fork this repo, make changes and submit pull request.