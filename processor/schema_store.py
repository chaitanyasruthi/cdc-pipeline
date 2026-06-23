import sqlite3
import json

DB_PATH = "/app/state/schemas.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS table_schemas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT,
        schema_version INTEGER,
        schema_definition TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def register_schema(table_name, schema_definition):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    schema_json = json.dumps(schema_definition, sort_keys=True)

    cur.execute(
        "SELECT schema_version FROM table_schemas WHERE table_name=? AND schema_definition=?",
        (table_name, schema_json)
    )

    row = cur.fetchone()

    if row:
        conn.close()
        return row[0]

    cur.execute(
        "SELECT MAX(schema_version) FROM table_schemas WHERE table_name=?",
        (table_name,)
    )

    latest = cur.fetchone()[0]
    version = 1 if latest is None else latest + 1

    cur.execute(
        """
        INSERT INTO table_schemas
        (table_name,schema_version,schema_definition)
        VALUES(?,?,?)
        """,
        (table_name, version, schema_json)
    )

    conn.commit()
    conn.close()

    return version