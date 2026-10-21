# SQL Quiz App

A web-based SQL learning application built with Python, Streamlit, and Supabase PostgreSQL. The application allows authenticated users to practice SQL by writing queries, executing them against a practice database, reviewing query results, and checking their answers.

## Live Application and Repository

- **Live application:** https://sql-quiz-app-tdsng2a8psutotyep8bjwn.streamlit.app/ 
- **GitHub repository:** https://github.com/MasomaSh/sql-quiz-app

## Project Overview

The purpose of this project is to provide an interactive environment for practicing SQL queries against a PostgreSQL database. Users can work through a five-question quiz, receive feedback on their answers, and view the results returned by their SQL statements.

The quiz is worth 20 points in total, with each question worth 4 points.

## Features

- **User authentication:** Users sign in through Supabase Auth before accessing quiz functionality.
- **Five-question SQL quiz:** Practice SQL through five questions worth 4 points each.
- **Interactive query execution:** Write and execute SQL queries against the practice database.
- **Query results:** View returned rows and columns directly in the application.
- **Answer checking:** Check answers against the requirements of each question and receive feedback when required SQL clauses or operations are missing.
- **Hints:** Use question-specific hints to guide query development.
- **SQL validation:** Queries must end with a semicolon before they can be run or checked.
- **Read-only query execution:** The SQL runner restricts execution to permitted `SELECT` and `WITH` statements.
- **Submission tracking:** Authenticated users can save their query submissions in PostgreSQL.
- **Automated checks:** GitHub Actions runs configured project tests and database connection checks.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and SQL execution |
| Streamlit | Web interface |
| Supabase PostgreSQL | Hosted relational database |
| Supabase Auth | User authentication |
| psycopg2 | PostgreSQL connectivity |
| pandas | Working with tabular query results |
| python-dotenv | Loading local environment variables |
| GitHub Actions | Automated testing and database connection checks |
| GitHub | Source control and project hosting |
| Streamlit Community Cloud | Application deployment |

## Database Design

The application connects to a Supabase-hosted PostgreSQL database containing the tables used for SQL practice.

The practice database includes:

- `customers`
- `products`
- `orders`

The `quiz_submissions` table stores authenticated users' submitted queries, including the user ID, question ID, query text, and submission timestamp.

The submission table references Supabase Auth users through `user_id`. Row Level Security (RLS) is enabled, with policies that restrict users to viewing and saving their own submissions.

## Security Measures

Security is an important part of this project.

- **Restricted database role:** The application connects using a dedicated PostgreSQL role with limited privileges rather than a database administrator account.
- **Protected credentials:** Database credentials are stored in local environment variables or deployment secrets rather than hardcoded in application files.
- **GitHub Actions secrets:** Database connection settings are provided through GitHub repository secrets.
- **Streamlit secrets:** Deployment configuration is stored in Streamlit Community Cloud secrets.
- **Supabase authentication:** Users must authenticate before accessing protected quiz functionality.
- **Row Level Security:** RLS policies restrict access to each user's own quiz submissions.
- **Read-only SQL execution:** The query runner permits only supported read-only SQL statements and uses a read-only transaction.
- **Execution safeguards:** Statement timeouts and a maximum returned-row limit help control query execution.
- **Version-control protection:** The `.env` file, virtual environment, and generated cache files are excluded through `.gitignore`.

Database credentials and private keys must never be committed to the repository.

## How to Use the Application

1. Open the deployed application using the live application link above.
2. Sign in with an existing account configured in Supabase Auth, or create a new account using the sign-up option.
3. Select a quiz question and read its instructions.
4. Review the hint if needed.
5. Write a SQL query in the editor.
6. End the query with a semicolon.
7. Run the query to view the returned results.
8. Check the answer and review the feedback.
9. Continue through the five quiz questions.

Each question is worth 4 points, for a total of 20 points.

## Local Setup and Installation

### Prerequisites

- Python installed on your computer
- Git
- A Supabase project with the required database tables, permissions, and authentication configuration

### 1. Clone the repository

```bash
git clone https://github.com/MasomaSh/sql-quiz-app.git
cd sql-quiz-app
```

### 2. Create a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory of the project.

Add the following variables using the values from your own Supabase project:

```dotenv
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=postgres
DB_USER=your-restricted-database-user
DB_PASSWORD=your-database-password
DB_SSLMODE=require

SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-supabase-publishable-key
```

Replace the example values with your actual configuration. Do not commit `.env` to GitHub or share database passwords.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically:

`http://localhost:8501`

## GitHub Actions and Automated Testing

GitHub Actions is used to run the project's configured automated checks. Database credentials are supplied through GitHub repository secrets, avoiding hardcoded passwords in the workflow.

The project includes scripts for checking database connectivity and verifying database tables.

To view workflow runs and their results, visit the repository's Actions tab:

https://github.com/MasomaSh/sql-quiz-app/actions

The workflow must be configured with the required repository secrets for database-dependent checks to succeed.

## Deployment

The application is deployed using Streamlit Community Cloud and connected to the GitHub repository.

The deployment uses the repository's `main` branch and `app.py` as its application entry point. Database and Supabase authentication configuration is supplied through Streamlit Community Cloud secrets.

To deploy your own instance:

1. Clone the repository.
2. Configure a Supabase project and create the required database tables and permissions.
3. Configure the required secrets in Streamlit Community Cloud.
4. Deploy `app.py` from the repository.
5. Open the application and verify authentication, query execution, answer checking, and submission saving.

## Project Structure

```text
sql-quiz-app/
├── app.py
├── db.py
├── sql_runner.py
├── quiz_questions.py
├── inspect_db.py
├── test_connection.py
├── test_tables.py
├── requirements.txt
├── README.md
└── .gitignore
```

- `app.py`: Streamlit user interface and quiz workflow.
- `db.py`: Database connection configuration and database utilities.
- `sql_runner.py`: SQL execution and query restrictions.
- `quiz_questions.py`: Quiz questions, hints, and answer requirements.
- `inspect_db.py`: Database inspection utility.
- `test_connection.py`: Database connectivity test.
- `test_tables.py`: Database table checks.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Excludes local configuration, secrets, and generated files.

## Future Improvements

Possible future enhancements include additional SQL questions, progress tracking, and a leaderboard.