"""
to be extended...
"""

import os
import yaml
from SmartHomeMyCastle import DataBaseAlchemy as DBAl
import config as conf
import logging

# Setting up logger                                         logger                      -   START   -
lg = logging.getLogger()
# Setting up logger                                         logger                      -   ENDED   -

lg.info("START     : {:>85} <<<".format('server_preparation.py'))


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


def server_data(source: str, filename: str = "server_preparation.py"):
    """=== Function name: fsh =====================================================================================
    Check and if missing create File System Hierarchy for Project
    :return:
    ============================================================================================== by Sziller ==="""
    data = {"path": source, "fn": filename}
    with open(data["path"], 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
            lg.info("prepare   : Loaded server_data from {path} - says {fn}".format(**data))
            return parsed_yaml
        except yaml.YAMLError as exc:
            lg.critical("Failed to load server_data from {path} - says {fn}".format(**data))
            raise(exc)
            
            

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

