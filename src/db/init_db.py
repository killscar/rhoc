"""Initialize the project's SQLite database."""

from pathlib import Path
import sqlite3

SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DB_PATH = Path(__file__).resolve().parents[2] / "db" / "episodes.sqlite"


def init_db(db_path: Path = DB_PATH, schema_path: Path = SCHEMA_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
