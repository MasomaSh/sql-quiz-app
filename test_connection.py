
from db import get_connection

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT current_user, current_database()"
        )
        print(cursor.fetchone())
