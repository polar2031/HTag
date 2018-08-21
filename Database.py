import sqlite3


class TagDatabase:
    def __init__(self, database_file_name):
        self.conn = sqlite3.connect(database_file_name)

    def is_database_exist(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='works';")
        # if new db: return 0
        if len(cursor.fetchall()) == 0:
            re = False
        else:
            re = True
        cursor.close()
        return re

    def build_database(self):
        cursor = self.conn.cursor()
        initial_commands = [
            # works table
            "CREATE TABLE works "
            "(id INTEGER PRIMARY KEY, "
            "name NTEXT NOT NULL)",
            # released works table
            "CREATE TABLE released_works "
            "(id INTEGER PRIMARY KEY, "
            "work_id INTEGER, "
            "FOREIGN KEY(work_id) REFERENCES works(id))"
        ]
        for command in initial_commands:
            cursor.execute(command)
        cursor.close()
        self.conn.commit()
