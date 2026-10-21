


import pandas as pd

from db import get_connection


MAX_ROWS = 200


def run_sql(query):
    """Run one read-only SQL query and return its results as a DataFrame."""

    if not query or not query.strip():
        raise ValueError("Please enter a SQL query.")

    query = query.strip()

    # Allow a trailing semicolon, but reject multiple statements.
    query = query.rstrip(";").strip()

    if not query:
        raise ValueError("Please enter a SQL query.")

    if ";" in query:
        raise ValueError("Please enter only one SQL statement.")

    # Keep the quiz runner focused on queries, not SQL scripts.
    if "--" in query or "/*" in query or "*/" in query:
        raise ValueError("SQL comments are not allowed in the quiz.")

    first_word = query.split(None, 1)[0].upper()

    if first_word not in {"SELECT", "WITH"}:
        raise ValueError("Only SELECT queries are allowed.")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            # PostgreSQL will reject changes in this transaction.
            cursor.execute("SET TRANSACTION READ ONLY")
            cursor.execute(query)

            if cursor.description is None:
                raise ValueError(
                    "Your query must return a result table."
                )

            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchmany(MAX_ROWS + 1)

            if len(rows) > MAX_ROWS:
                raise ValueError(
                    f"Your query returned more than {MAX_ROWS} rows. "
                    "Please narrow your results."
                )

    return pd.DataFrame(rows, columns=columns)
