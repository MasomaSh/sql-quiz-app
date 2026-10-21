
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    required = ["DB_HOST", "DB_USER", "DB_PASSWORD"]
    missing = [key for key in required if not os.getenv(key)]

    if missing:
        raise ValueError(
            "Missing database settings: " + ", ".join(missing)
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "require"),
        connect_timeout=10,
        options="-c statement_timeout=5000",
    )
