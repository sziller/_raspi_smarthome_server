"""
to be extended...
"""

import os
import sqlite3 as sql
from MyHomeMyCastle import DataBaseAlchemy as DBAl
import config as conf


def fsh():
    """=== Function name: fsh =====================================================================================
    Check and if missing create File System Hierarchy for Project
    :return:
    ============================================================================================== by Sziller ==="""
    print("[  START]: Necessary FileSystemHierarchy check")
    for dirname in conf.NECESSARY_DIRECTORIES:
        if not os.path.exists(dirname):
            print("[  START]: New directory created: {}".format(dirname))
            os.mkdir(dirname)
    print("[  ENDED]: Necessary FileSystemHierarchy check")


def db(db_to_check):
    """=== Function name: db ======================================================================================
    Function receives a list of DataBase paths and creates the ones which do not exist.
    :return:
    ============================================================================================== by Sziller ==="""
    print("[  START]: Database management")
    if not os.path.isfile(db_to_check):
        db_connection = sql.connect(db_to_check)
        db_cursor = db_connection.cursor()
        with open(conf.DATABASE_SETUP_SCRIPT) as file:
            sql_script = file.read()
        db_cursor.executescript(sql_script)
        db_cursor.close()
        db_connection.close()
    print("[  ENDED]: Database management")


def default_users(session_in):
    """=== Function name: default_users ============================================================================

    :return:
    ========================================================================================== by Sziller ==="""
    print("[  START]: Adding default users: {}".format(conf.DATABASE_STYLE))
    default_user_list = conf.DEFAULT_USER_LIST
    DBAl.ADD_rows_to_table(
        primary_key="uuid",
        data_list=default_user_list,
        db_table=conf.DB_ID_TABLE_USERS,
        session_in=session_in)
    print("[  ENDED]: Adding default users: {}".format(conf.DATABASE_STYLE))

