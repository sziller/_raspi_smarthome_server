"""
to be extended...
"""

import os
import yaml
from shmc_sqlAccess import SQL_interface as SQLi
import config as conf
import logging

# Setting up logger                                         logger                      -   START   -
lg = logging.getLogger()
# Setting up logger                                         logger                      -   ENDED   -

lg.info("START     : {:>85} <<<".format('session_preparation.py'))


def fsh(dir_list: list[str]):
    """=== Function name: fsh =====================================================================================
    Check and if missing create File System Hierarchy for Project
    :return:
    ============================================================================================== by Sziller ==="""
    lg.debug("fsh check : Necessary FileSystemHierarchy check - START")
    for dirname in dir_list:
        if not os.path.exists(dirname):
            lg.warning("fsh update: New directory created: {}".format(dirname))
            os.mkdir(dirname)
    lg.debug("fsh check : Necessary FileSystemHierarchy check - ENDED")


def read_yaml_data(source: str):
    """=== Function name: fsh =====================================================================================
    Check and if missing create File System Hierarchy for Project
    :return:
    ============================================================================================== by Sziller ==="""
    data = {"path": source, "fn": os.path.basename(__file__)}
    with open(data["path"], 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
            lg.info("prepare   : Loaded server_data from {path} - says {fn}".format(**data))
            return parsed_yaml
        except yaml.YAMLError as exc:
            lg.critical("Failed to load server_data from {path} - says {fn}".format(**data))
            raise exc
            
            
# def default_users(session_in):
#     """=== Function name: default_users ============================================================================
# 
#     :return:
#     ========================================================================================== by Sziller ==="""
#     print("[  START]: Adding default users: {}".format(conf.DATABASE_STYLE))
#     default_user_list = conf.DEFAULT_USER_LIST
#     SQLi.ADD_rows_to_table(
#         primary_key="uuid",
#         data_list=default_user_list,
#         db_table=conf.DB_ID_TABLE_USERS,
#         session_in=session_in)
#     print("[  ENDED]: Adding default users: {}".format(conf.DATABASE_STYLE))

