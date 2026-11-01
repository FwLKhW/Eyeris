# # uv run python -m tests.manual.test_fts5_support

import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

try:
    cursor.execute("SELECT sqlite_version();")
    print(f"SQLite Version: {cursor.fetchone()[0]}")

    cursor.execute("CREATE VIRTUAL TABLE tech_books USING fts5(title, description);")
    print("supported")
except sqlite3.OperationalError:
    print("not supported")
