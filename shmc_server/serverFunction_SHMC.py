"""
This is an umbrella server application for the MHMC project. It uses different routers, that neew to be installed
 alongside the server in <shmc_routers>.
This server setup can be used for any collection / combination of routers it the MHMC project.
USE THIS API as entry point whether on an umbrella router or on local terminals.

<shmc_routers> is both a locally kept package for development reasons and also an installable package. 

ATTENTION: we operate with a subserver here! For details: https://fastapi.tiangolo.com/advanced/sub-applications/
In short: <server> is the outer shell serving all requests, underneath which <app> handles the server logic.
1. Server:
1.1 Static
1.2 App
1.2.1 aqua
1.2.2 obsr
1.2.3 room

FastAPI hints:
- Typing is absolutely necessary in python
- main scope: initiate global Processes and Objects here
"""

import os
import yaml
from time_format import TimeFormat as TiFo
from dotenv import load_dotenv
import logging
import config as conf
import config_prv as conf_prv
import importlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from shmc_sqlAccess.SQL_interface import createSession
from shmc_sqlAccess import SQL_interface as SQLi
from shmc_sqlBases.sql_baseUser import User as sqlUser
from sqlalchemy.orm import sessionmaker
# from shmc_server import session_preparation as prepare

# -------------------------------------------------------------------------------------------------------------------
# - Additional functions                                                                                -   START   -
# -------------------------------------------------------------------------------------------------------------------


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


def db(session: sessionmaker.object_session, user_list: list) -> bool:
    """

    :param session: 
    :param user_list: 
    :return: 
    """
    lg.warning("user db   : entering default users - if not included!")
    SQLi.ADD_rows_to_table(primary_key="username", data_list=user_list, row_obj=sqlUser, session=session)
    return True

# -------------------------------------------------------------------------------------------------------------------
# - Additional functions                                                                                -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------


# READ BASIC SETTINGS                                                                   -   START   -
# from .env:
load_dotenv()
# Mount settings:
mount_script = os.getenv("PATH_MOUNTSHARES")
# DB settings:
session_name_shmc   = os.getenv("DB_FULLNAME_SHMC")
session_style_shmc  = os.getenv("DB_STYLE_SHMC")
session_name_auth   = os.getenv("DB_FULLNAME_AUTH")
session_style_auth  = os.getenv("DB_STYLE_AUTH")
# from config.py:
# language settings:
LNG                 = conf.LANGUAGE_CODE
# path settings:
fsh_dir_info                    = conf.NECESSARY_DIRECTORIES
path_root                       = conf.PATH_ROOT
path_err_msg                    = conf.PATH_ERROR_MSG.format(path_root)
path_app_doc                    = conf.PATH_APP_INFO.format(path_root)
path_mount_static_from          = conf.PATH_STATIC_FROM
path_mount_static_to            = conf.PATH_STATIC_TO
# log settings:
log_format = conf.LOG_FORMAT
log_level = getattr(logging, conf.LOG_LEVEL)
log_ts = "_{}".format(TiFo.timestamp()) if conf.LOG_TIMED else ""
log_tf = conf.LOG_TIMEFORMAT
log_path = conf.LOG_PATH.format(path_root)
log_fullfilename = conf.LOG_FILENAME.format(log_path, log_ts)
# app settings:
app_id              = conf.APP_ID
app_path            = conf.APP_PATH
# READ BASIC SETTINGS                                                                   -   ENDED   -

# Setting up logger                                                                     -   START   -
if not os.path.exists(log_path): os.mkdir(log_path)
lg = logging.getLogger("shmc")
# Using config.py data - configurate logger:
logging.basicConfig(filename=log_fullfilename, level=log_level, format=log_format, datefmt=log_tf, filemode="w")
# initial messages
lg.warning("FILE: {:>86} <<<".format(__file__))
lg.warning("LOGGER namespace: {:>74} <<<".format(__name__))
lg.debug("listing   : config settings:")
for k, v in {param: arg for param, arg in vars(conf).items() if not param.startswith('__')}.items():
    lg.debug("{:>20}: {}".format(k, v))
# Setting up logger                                                                     -   ENDED   -

# Main App messages:
lg.warning("          : ============================================")
lg.warning({True:  "          : =               LIVE SESSION               =",
            False: "          : =               DEV  SESSION               ="}[conf.isLIVE])
lg.warning("          : ={:^42}=".format(__name__))
lg.info("          : =            user languange: {}            =".format(LNG))
lg.warning("          : ============================================")

lg.warning("mount-os  : Local DB-s to server filesystem")

# Run the bash script
# output = os.popen('bash {}'.format(mount_script)).read()
# lg.warning(output)

# prepare script running:                                                           -   START   -
lg.info("setup fsh : {}".format(fsh_dir_info))
fsh(fsh_dir_info)
lg.info("read data : from: {}".format(path_err_msg))
err_msg  = read_yaml_data(source=path_err_msg)
lg.info("read data : from: {}".format(path_app_doc))
APP_INFO = read_yaml_data(source=path_app_doc)
# prepare script running:                                                           -   ENDED   -
# -------------------------------------------------------------------------------------------------------
# - Basic setup                                                                      START              -
# -------------------------------------------------------------------------------------------------------

# server data processing:                                                           -   START   -
lg.info("read conf.: APP_ROUTER_INFO")
router_info = conf.APP_ROUTER_INFO
lg.info("arrange   : tags_metadata")
tags_metadata = []
for name, data in router_info.items():
    if data["use"]:
        data["name"] = name
        tags_metadata.append(data)
# server data processing:                                                           -   ENDED   -

# server base DB session:                                                           -   START   -
session_shmc = createSession(db_fullname=session_name_shmc, tables=None,                style=session_style_shmc)
session_auth = createSession(db_fullname=session_name_auth, tables=[sqlUser.__table__], style=session_style_auth)
db(session=session_auth, user_list=conf_prv.DEFAULT_USER_LIST)
session_shmc.close()
session_auth.close()

# server base DB session:                                                           -   ENDED   -

# -------------------------------------------------------------------------------------------------------
# - Basic setup                                                                     ENDED              -
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   START   -
# -------------------------------------------------------------------------------------------------------

lg.info("init.     : server = FastAPI - using configuration and text data")

server = FastAPI()
app = FastAPI(openapi_tags=tags_metadata,
              title=APP_INFO["proj_name"],
              version=APP_INFO["version"],
              summary=APP_INFO["summary"],
              description=APP_INFO["description"],
              contact={"name": "SmartHomeMyCastle",
                       "email": "szillerke@gmail.com"},
              terms_of_service=APP_INFO["terms"],
              openapi_url=APP_INFO["url"].format(APP_INFO["proj_nick"]))
server.mount(path=app_path, app=app, name="shmc")

# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   ENDED   -
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
# StaticFiles                                                                               -   START   -
# -------------------------------------------------------------------------------------------------------

# ATTENTION: mounting StaticFiles over the path you use for your server, will mess up your routing-paths,
# and "details: not found" message will indicate, you're routing is wrong."

# path: sets the string you must type into the browser, when accessing data. You may want to "act" asif it was in a
# subdirectory, where it isn't, or show the actual subdirectory if necessary.
# by entering "/", you ensure the browser finds it under: host:0000/... directly
# app contains the 'directory' parameter, which must have the actual subdirectory as an argument
# if you call your basic page 'index.html' it can be accessed directly, without entering the actual filename


# Route handler for the root URL
server.mount(path="/", app=StaticFiles(directory="public", html=True), name="public")

# @app.get("/")
# async def read_index():
#     """
# 
#     :return: 
#     """
#     # Get the path to the index.html file
#     index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "index.html")
#     # Check if the file exists
#     if os.path.exists(index_path):
#         # Return the index.html file as a response
#         return FileResponse(index_path)
#     else:
#         # Return a simple message if index.html does not exist
#         return {"message": "index.html not found"}

# server.mount(path="/", app=StaticFiles(directory="public", html=True), name="public")
lg.warning("mount-srvr: StaticDeta from '{}' to '{}'".format(path_mount_static_from, path_mount_static_to))

# -------------------------------------------------------------------------------------------------------
# StaticFiles                                                                               -   ENDED   -
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   START   -
# -------------------------------------------------------------------------------------------------------------------
ROUTER_OBJECTS = {}

for name, data in router_info.items():  # looping through routing_info as key, value
    if data['use']:
        try:
            # we import the class named: (change here to modify class name definition)
            class_name = data['module'].split(sep=".")[1].split(sep="_")[0]
            # we import the class from the <module>:
            router_class = getattr(importlib.import_module(data['module']), class_name)
            # we instantiate it:
            alias = data["prefix"][1:]
            # sufix = ""
            # if "args" in data and data["args"]["ip"] != "localhost":
            sufix = "_" + alias.upper()
            lg.debug("fetch args: 'alias': {}, 'sufix': {}".format(alias, sufix))
            lg.debug("initiating: <router> from {}".format(os.path.basename(__file__)))
            router_instance = router_class(name=name,
                                           alias=alias,
                                           db_fullname=os.getenv("DB_FULLNAME{}".format(sufix)),
                                           db_style=os.getenv("DB_STYLE{}".format(sufix)))
            # we set arguments for the instance:
            if "args" in data and data["args"]:
                for param, arg in data["args"].items():
                    setattr(router_instance, param, arg)
                    lg.debug("set router: '{}' - set: {} : {}".format(name, param, arg))
                router_instance.reinit()
                    
            # collect instances under their names:
            ROUTER_OBJECTS[name] = router_instance
            lg.info("add router: {} as {}.router() - under {}".format([name], data["module"], data["prefix"]))
            # add router instances to the <app> sub-server:
            app.include_router(router=router_instance, tags=[name], prefix=data["prefix"])
            lg.info("incl.rout.: {}".format(router_instance))
        except (ImportError, AttributeError):
            msg = err_msg[103][LNG].format(name)
            lg.error(msg)
lg.debug("SUMMARY   : --------------------------------------------------------------------------------")
lg.debug("listing   : all routers included in <app> sub-server:")
for k, v in ROUTER_OBJECTS.items():
    lg.debug("      >>> :{:>12}: {}".format(k, v))

lg.warning("running   : SERVER from {}".format(__file__))

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------
