import sqlite3

conn = sqlite3.connect("../state/schemas.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS table_schemas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
table_name TEXT,
schema_version INTEGER,
schema_definition TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()