import sqlite3
from typing import Any
import os

class OnebotDatabase:
    def __init__(self, path) -> None:
        self.path = path
    
    def __call__(self, file: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        con = sqlite3.connect(os.path.join(self.path, file))
        cur = con.cursor()
        return con, cur

    def create_table(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
        cur.execute(
	                "CREATE TABLE IF NOT EXISTS"
	                "{}(id INTEGER PRIMARY KEY AUTOINCREMENT,"
	                "{} INTEGER, {} REAL, {} TEXT, {} TEXT)"
	                .format()
                    )
        con.commit()
        
    def add_data(self, con: sqlite3.Connection, cur: sqlite3.Cursor, table: str, data: tuple[Any]) -> None:
        cur.execute(
                    "INSERT INTO {} VALUES (?, ?, ?, ?)"
                    .format(table),
                    data
                    )
        con.commit()
    
    def get_data(self, con: sqlite3.Connection, cur: sqlite3.Cursor, content: str, table: str) -> list[tuple[Any]]:
        cur.execute("SELECT {} FROM {}".format(content, table))
        return cur.fetchall()
    
    def update_data(self, con: sqlite3.Connection, cur: sqlite3.Cursor, table: str, content: str, data: tuple[Any]) -> None:
        cur.execute(
                    "UPDATE {} SET {}=? WHERE id=?"
                    .format(table, content),
                    data
                    )
        con.commit()
        
    def delete_data(self, con: sqlite3.Connection, cur: sqlite3.Cursor, table: str, id: int) -> None:
        cur.execute(
                    "DELETE FROM {} WHERE id=?"
                    .format(table),
                    (id,)
                    )
        con.commit()
        
    def delete_table(self, con: sqlite3.Connection, cur: sqlite3.Cursor, table: str) -> None:
        cur.execute("DROP TABLE {}".format(table))
        con.commit()
    
    def close(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
        cur.close()
        con.close()