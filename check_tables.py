
from db.database import get_connection

with get_connection() as connection:
    cursor = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = ?",
        ("table",)
    )

    tables = [
        row["name"]
        for row in cursor.fetchall()
        if not row["name"].startswith("sqlite_")
    ]

print("Database tables:")
for table in tables:
    print("-", table)
