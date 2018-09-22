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
            # 原作品
            # ID, 作品名
            "CREATE TABLE work "
            "(id INTEGER PRIMARY KEY, "
            "name NTEXT NOT NULL)",

            # released_work X works table
            # 釋出作品 X 原作品
            # 釋出作品ID, 原作品ID
            "CREATE TABLE released_work_x_work "
            "(released_work_id INTEGER, "
            "work_id INTEGER)",

            # released_work table
            # 釋出作品
            # ID, 全名
            "CREATE TABLE released_work "
            "(id INTEGER PRIMARY KEY, "
            "name NTEXT NOT NULL)",

            # released_work X releaser
            # 釋出作品 X 釋出者
            # 釋出作品ID, 釋出者ID
            "CREATE TABLE released_work_x_releaser "
            "(released_work_id INTEGER, "
            "releaser_id INTEGER)",

            # released_work X path
            # 釋出作品 X 檔案路徑
            # 釋出作品ID, 檔案路徑
            "CREATE TABLE released_work_x_path "
            "(released_work_id INTEGER, "
            "path NTEXT)",

            # work X author
            # 原作品 X 作者
            # 原作品ID, 作者ID
            "CREATE TABLE work_x_author "
            "(work_id INTEGER, "
            "author_id INTEGER)",

            # author table
            # 作者
            # 作者ID, 作者名
            "CREATE TABLE author "
            "(id INTEGER PRIMARY KEY, "
            "name NTEXT NOT NULL)"
        ]
        for command in initial_commands:
            cursor.execute(command)
        cursor.close()
        self.conn.commit()

    def search_author(self, author):
        cursor = self.conn.cursor()
