
import os
import re

import chromadb
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = "sql_quiz_schema"
GEMINI_MODEL = "gemini-3.8-flash"

# Actual database schema obtained from inspect_db.py.
SCHEMA_DOCUMENTS = [
    """
    Table: customers
    Purpose: Stores customer information.
    Columns:
    - customer_id: integer, customer identifier
    - customer_name: text, customer's name
    - city: text, customer's city
    """,
    """
    Table: products
    Purpose: Stores product information.
    Columns:
    - product_id: integer, product identifier
    - product_name: text, product name
    - category: text, product category
    - price: numeric, product price
    """,
    """
    Table: orders
    Purpose: Stores customer orders.
    Columns:
    - order_id: integer, order identifier
    - customer_id: integer, customer identifier
    - product_id: integer, product identifier
    - quantity: integer, quantity ordered
    The customer_id and product_id columns can be used to match
    orders with customers and products using their corresponding IDs.
    """,
]


def get_collection():
    """Create the ChromaDB collection and update its schema documents."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "SQL quiz database schema"},
    )

    # Refresh the stored schema documents.
    collection.upsert(
        ids=[f"schema_{i}" for i in range(len(SCHEMA_DOCUMENTS))],
        documents=SCHEMA_DOCUMENTS,
    )

    return collection


def retrieve_schema(question: str, n_results: int = 3) -> list[str]:
    """Retrieve schema documents relevant to the user's question."""
    collection = get_collection()
    document_count = collection.count()

    if document_count == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, document_count),
    )

    return results.get("documents", [[]])[0]


def clean_generated_sql(sql: str) -> str:
    """Remove Markdown formatting and perform basic SQL output checks."""
    sql = sql.strip()

    # Remove Markdown code fences, including ```sql fences.
    if sql.startswith("```"):
        lines = sql.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        sql = "\n".join(lines).strip()

    # Remove inline Markdown bold markers, such as **SUM**.
    sql = sql.replace("**", "")

    # Remove inline code backticks if the model adds them.
    sql = sql.replace("`", "")

    # Remove an optional SQL label at the beginning.
    sql = re.sub(r"^\s*sql\s*[\r\n]+", "", sql, flags=re.IGNORECASE)

    sql = sql.strip()

    if not sql:
        raise ValueError("The AI returned an empty SQL query.")

    # Require a single SELECT statement.
    if not re.match(r"^SELECT\b", sql, flags=re.IGNORECASE):
        raise ValueError(
            "The AI response is not a SELECT statement. "
            "Please try rephrasing your question."
        )

    # Require a trailing semicolon.
    if not sql.endswith(";"):
        raise ValueError(
            "The generated SQL is missing a semicolon at the end. "
            "Please generate the query again."
        )

    # Basic check for multiple SQL statements.
    # This is a formatting check, not a complete SQL security validator.
    if ";" in sql[:-1]:
        raise ValueError(
            "The AI returned more than one SQL statement. "
            "Please generate the query again."
        )

    return sql


def generate_sql(question: str) -> tuple[str, list[str]]:
    """Generate read-only PostgreSQL SQL using retrieved schema context."""
    question = question.strip()

    if not question:
        raise ValueError("Please enter a question before generating SQL.")

    api_key = os.getenv("GEMINI_API_KEY")

    try:
        api_key = st.secrets.get("GEMINI_API_KEY") or api_key
    except Exception:
        # Streamlit Secrets may not be configured locally.
        pass

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your local .env "
            "file or your deployed app's Streamlit Secrets."
        )

    context = retrieve_schema(question)

    if not context:
        raise ValueError("No database schema context was retrieved.")

    prompt = f"""
You are a SQL tutor for a PostgreSQL database.

Translate the user's natural-language question into SQL using only
the tables, columns, and relationships supported by the schema context.

Rules:
- Use only tables and columns listed in the retrieved schema.
- Do not invent column names or relationships.
- Use PostgreSQL syntax.
- Generate exactly one read-only SELECT statement when the schema
  supports the request.
- The SQL statement must end with a semicolon.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
  or any other data-changing statement.
- If the retrieved context is insufficient, briefly explain what
  schema information is missing instead of guessing.
- Return plain SQL only.
- Do not use Markdown, code fences, or bold formatting.
- Do not wrap SQL function names in Markdown markers.

Retrieved schema context:
{chr(10).join(context)}

User question:
{question}
"""

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    raw_sql = response.text or ""

    # Clean the model output and check its basic format.
    sql = clean_generated_sql(raw_sql)

    return sql, context
