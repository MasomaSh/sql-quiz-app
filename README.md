# SQL Quiz App with RAG-Powered SQL Generation

A web-based SQL learning application built with Python, Streamlit, Supabase PostgreSQL, ChromaDB, and Gemini API. The application combines an interactive SQL quiz with Retrieval-Augmented Generation (RAG), allowing users to practice SQL queries and generate SQL from natural-language questions.

## Live Application and Repository

- **Live application:** https://sql-quiz-app-tdsng2a8psutotyep8bjwn.streamlit.app/
- **GitHub repository:** https://github.com/MasomaSh/sql-quiz-app

## Project Overview

This project is an interactive SQL learning application that combines a PostgreSQL-based SQL quiz with an AI-powered SQL generation feature.

The original application allows authenticated users to practice SQL by writing queries, executing them against a PostgreSQL practice database, reviewing query results, and checking their answers.

The application has been extended with Retrieval-Augmented Generation (RAG), allowing users to enter questions in natural language and receive AI-generated SQL queries. The RAG pipeline uses ChromaDB to retrieve relevant database schema information and the Gemini API to generate SQL based on the retrieved context.

The quiz consists of five questions, with each question worth 4 points and a total possible score of 20 points.

## Features

### SQL Quiz Application

- **User authentication:** Users sign in through Supabase Auth before accessing quiz functionality.
- **Five-question SQL quiz:** Practice SQL through five questions worth 4 points each.
- **Interactive query execution:** Write and execute SQL queries against the practice database.
- **Query results:** View returned rows and columns directly in the application.
- **Answer checking:** Check answers against the requirements of each question and receive feedback when required SQL clauses or operations are missing.
- **Hints:** Use question-specific hints to guide query development.
- **SQL validation:** Queries must end with a semicolon before they can be run or checked.
- **Read-only query execution:** The SQL runner restricts execution to permitted SELECT and WITH statements.
- **Submission tracking:** Authenticated users can save their query submissions in PostgreSQL.
- **Automated checks:** GitHub Actions runs configured project tests and database connection checks.

### AI-Powered SQL Generation (RAG)

- **Natural-language input:** Enter questions about the practice database without writing SQL.
- **Vector database:** Store database schema information in ChromaDB.
- **Semantic retrieval:** Retrieve relevant schema information based on the meaning of the user's question.
- **AI-powered SQL generation:** Use Gemini API to generate SQL queries using the retrieved context.
- **Context-aware generation:** Provide the AI model with relevant table and column information before generating SQL.

## RAG Architecture

The application extends the original SQL Quiz with a Retrieval-Augmented Generation (RAG) pipeline that converts natural-language questions into SQL queries.

### Technologies Used

- **Supabase PostgreSQL:** Stores the relational practice database, including customers, products, and orders.
- **ChromaDB:** Stores database schema information as vector embeddings and retrieves relevant context through semantic similarity search.
- **Gemini API:** Generates SQL queries using the user's natural-language question and the context retrieved from ChromaDB.

### RAG Workflow

The SQL generation process follows these steps:

1. **User question:** The user enters a natural-language question related to the practice database.
2. **Vector retrieval:** The application searches the ChromaDB collection for relevant schema information.
3. **Context retrieval:** ChromaDB returns the most relevant database schema information based on semantic similarity.
4. **Prompt construction:** The retrieved context and original question are combined into a prompt.
5. **SQL generation:** The Gemini API uses the provided context to generate an SQL query.
6. **Output:** The generated SQL query is displayed in the Streamlit application.

**Workflow:**

User Question → ChromaDB Vector Retrieval → Retrieved Schema Context → Gemini API → Generated SQL Query

The vector retrieval step provides relevant database knowledge to the language model instead of relying only on its general knowledge.

### Vector Database Design

The application uses a ChromaDB collection named `sql_quiz_schema` to store embedded database schema information.

The collection contains information about the practice database tables, including:

- `customers`
- `products`
- `orders`

When a user submits a natural-language question, the application performs a similarity search against the stored schema information. The retrieved documents are then passed to Gemini to support SQL generation.

ChromaDB handles semantic retrieval, while Supabase PostgreSQL remains the primary relational database.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and SQL generation |
| Streamlit | Web interface |
| Supabase PostgreSQL | Hosted relational database |
| Supabase Auth | User authentication |
| psycopg2 | PostgreSQL connectivity |
| pandas | Working with tabular query results |
| ChromaDB | Vector database and semantic retrieval |
| Gemini API | AI-powered SQL generation |
| Embedding model | Converts schema information and questions into vectors |
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

### Vector Database

In addition to PostgreSQL, the application uses ChromaDB as a vector database.

The `sql_quiz_schema` collection stores embedded database schema information for semantic retrieval. When a user submits a natural-language question, ChromaDB retrieves relevant schema information, which is provided to Gemini to generate an SQL query.

PostgreSQL and ChromaDB serve different purposes:

- PostgreSQL stores and manages relational data.
- ChromaDB stores and retrieves vector representations of database knowledge.

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
- **Version-control protection:** The `.env` file, virtual environment, local secrets, and generated cache files are excluded through `.gitignore`.
- **API key protection:** Gemini API keys are stored in environment variables or deployment secrets and are never committed to GitHub.

Database credentials and private API keys must never be committed to the repository.

## How to Use the Application

### SQL Quiz

1. Open the deployed application using the live application link.
2. Sign in with an existing account configured in Supabase Auth, or create a new account using the sign-up option.
3. Select a quiz question and read its instructions.
4. Review the hint if needed.
5. Write a SQL query in the editor.
6. End the query with a semicolon.
7. Run the query to view the returned results.
8. Check your answer and review the feedback.
9. Continue through the five quiz questions.

Each question is worth 4 points, for a total of 20 points.

### AI-Powered SQL Generation

1. Open the deployed application and sign in.
2. Navigate to the AI SQL generation feature.
3. Enter a natural-language question related to the practice database.
4. Submit the question.
5. The application retrieves relevant schema information from ChromaDB.
6. Gemini uses the retrieved context to generate an SQL query.
7. Review the generated SQL displayed in the application.

The generated query can be reviewed and, if supported by the application workflow, tested against the PostgreSQL practice database.

## Local Setup and Installation

### Prerequisites

- Python installed on your computer
- Git
- A Supabase project with the required database tables, permissions, and authentication configuration
- A Gemini API key

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

```env
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=postgres
DB_USER=your-restricted-database-user
DB_PASSWORD=your-database-password
DB_SSLMODE=require

SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-supabase-publishable-key

GEMINI_API_KEY=your-gemini-api-key
```

Replace the example values with your actual configuration. Use the exact environment variable names expected by your application.

Do not commit `.env` to GitHub or share database passwords and API keys.

### 5. Initialize the Vector Database

The RAG component uses ChromaDB to store and retrieve database schema information.

The application initializes a ChromaDB collection named `sql_quiz_schema` and populates it with the relevant schema information used during SQL generation.

Ensure that the collection is initialized and populated before performing vector retrieval.

The local ChromaDB persistence directory is configured as:

```text
./chroma_db
```

### 6. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically:

```text
http://localhost:8501
```

## GitHub Actions and Automated Testing

GitHub Actions is used to run the project's configured automated checks.

Database credentials are supplied through GitHub repository secrets, avoiding hardcoded passwords in the workflow.

The project includes scripts for checking database connectivity and verifying database tables.

To view workflow runs and their results, visit the repository's Actions tab:

https://github.com/MasomaSh/sql-quiz-app/actions

The workflow must be configured with the required repository secrets for database-dependent checks to succeed.

## Deployment

The application is deployed using Streamlit Community Cloud and connected to the GitHub repository.

The deployment uses the repository's main branch and `app.py` as its application entry point.

### Deployment Configuration

The deployed application requires:

- Supabase database credentials and authentication settings.
- Gemini API key.
- ChromaDB initialization and schema embedding configuration.
- Required Python dependencies.

Database credentials and the Gemini API key must be configured through Streamlit Community Cloud secrets.

The ChromaDB collection must be initialized and populated in the deployed environment for semantic retrieval to work. Local ChromaDB files are not automatically available in Streamlit Community Cloud.

### Deploying Your Own Instance

1. Clone the repository.
2. Configure a Supabase project and create the required database tables and permissions.
3. Obtain a Gemini API key.
4. Configure the required secrets in Streamlit Community Cloud.
5. Ensure the application initializes the ChromaDB collection and stores the schema embeddings.
6. Deploy `app.py` from the repository.
7. Open the application and verify authentication, quiz functionality, vector retrieval, and SQL generation.

## Screenshots

### SQL Quiz Application

This screenshot demonstrates the interactive SQL quiz interface and query execution functionality.

![SQL Quiz Interface](screenshots/sql-quiz.png)

### AI-Powered SQL Generation

This screenshot demonstrates a natural-language question submitted to the application and the SQL query generated using ChromaDB retrieval and the Gemini API.

![RAG SQL Generation](screenshots/rag-sql-generation.png)

## Project Structure

```text
sql-quiz-app/
├── app.py
├── db.py
├── sql_runner.py
├── quiz_questions.py
├── rag.py
├── inspect_db.py
├── test_connection.py
├── test_tables.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml
```

### File Descriptions

- `app.py`: Streamlit user interface and quiz workflow.
- `db.py`: Database connection configuration and database utilities.
- `sql_runner.py`: SQL execution and query restrictions.
- `quiz_questions.py`: Quiz questions, hints, and answer requirements.
- `rag.py`: ChromaDB retrieval and Gemini-powered SQL generation.
- `inspect_db.py`: Database inspection utility.
- `test_connection.py`: Database connectivity test.
- `test_tables.py`: Database table checks.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Excludes local configuration, secrets, and generated files.

The project structure may include additional files depending on the implementation.

## Future Improvements

Possible future enhancements include:

- Additional SQL quiz questions and difficulty levels.
- Improved schema linking and business-context retrieval.
- More few-shot examples to improve SQL generation.
- Automatic execution and validation of AI-generated SQL queries.
- Progress tracking and a leaderboard.
- Support for additional database schemas and natural-language questions.

**Note:** The AI SQL Assistant may take approximately 45-90 seconds to retrieve the relevant database schema from ChromaDB and generate the SQL query using Gemini. Please wait for the process to complete.