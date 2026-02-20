import sqlite3
from typing import List, Tuple, Any
from config import DB_PATH


class Queries:
    def _connect(self):
        return sqlite3.connect(DB_PATH)

    # -------------------------
    # Basic Select *
    # -------------------------
    def select_all_events(self) -> List[Tuple[Any]]:
        print("QUERY DB PATH:", DB_PATH)

        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()

        conn.close()
        return rows