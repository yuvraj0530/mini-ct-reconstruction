from db.database import get_connection

with get_connection() as connection:
    scan = connection.execute(
        "SELECT * FROM scans ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if scan is None:
        print("No scan found.")
    else:
        scan_id = scan["id"]
        print("Latest Scan ID:", scan_id)

        tables = [
            "phantoms",
            "beam_configs",
            "measurements",
            "reconstructions"
        ]

        for table in tables:
            rows = connection.execute(
                f"SELECT * FROM {table} WHERE scan_id = ?",
                (scan_id,)
            ).fetchall()

            print(f"{table}: {len(rows)} record(s)")