
from db import get_connection

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute("SET TRANSACTION READ ONLY")

        for table in ["customers", "products", "orders"]:
            cursor.execute(f"SELECT COUNT(*) FROM public.{table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} rows")
