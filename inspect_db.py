

from db import get_connection

tables = ["customers", "products", "orders"]

with get_connection() as connection:
    with connection.cursor() as cursor:
        for table in tables:
            print(f"\n--- {table} ---")

            cursor.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                ORDER BY ordinal_position
                """,
                (table,),
            )

            for column in cursor.fetchall():
                print(column)

            cursor.execute(f"SELECT * FROM public.{table} LIMIT 3")
            print("Sample rows:")
            for row in cursor.fetchall():
                print(row)
