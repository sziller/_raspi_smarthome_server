"""

"""
import config as conf
from MyHomeMyCastle import DataBaseAlchemy as DBAl

if __name__ == "__main__":
    print("--- reseting: SQLite ---")
    delete = [
        "scheduledtasks",
        # "merkletrees",
        # "users",
        # "documents",
        # "records"
    ]
    DBAl.db_delete_table(conf.DATABASE_NAME, dellist=delete, style="SQLite")

# in order to fully reset DB, you'll need to stop all queries in the DB directly (over DO - manually)
