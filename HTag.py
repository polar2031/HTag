import Database
import Works
import sys
import traceback


def main():
    # db = Database.TagDatabase("data.db")
    db = Database.TagDatabase(":memory:")
    if not db.is_database_exist():
        db.build_database()


if __name__ == '__main__':
    sys.exit(main())
