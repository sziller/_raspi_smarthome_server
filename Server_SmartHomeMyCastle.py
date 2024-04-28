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
import logging
import importlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from shmc_server import server_preparation as prepare
import config as conf

# Setting up language                                                                   -   START   -
LNG = conf.LANGUAGE_CODE
# Setting up language                                                                   -   ENDED   -

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
logging.basicConfig(filename="./log/srvr_shmc.log", level=logging.NOTSET, filemode="w",
                    format="%(asctime)s [%(levelname)8s]: %(message)s", datefmt='%y%m%d %H:%M:%S')
# Setting up logger                                                                     -   ENDED   -

lg.warning("START: {:>85} <<<".format('__name__ == "__main__" namespace: Server_SmartHomeMyCastle.py'))
lg.warning("          : ======================================")
lg.warning({True:  "          : =            LIVE SESSION            =",
            False: "          : =            DEV  SESSION            ="}[conf.isLIVE])
lg.warning("          : ={:^36}=".format(__name__))
lg.info("          : =         user languange: {}         =".format(LNG))
lg.warning("          : ======================================")

# -------------------------------------------------------------------------------------------------------
# - Basic setup                                                                      START              -
# -------------------------------------------------------------------------------------------------------

lg.info("prepare   : Actions taken for {} version.".format({True: "LIVE", False: " DEV"}[conf.isLIVE]))

# -------------------------------------------------------------------------------------------------------
# -                                                                                 ENDED              -
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   START   -
# -------------------------------------------------------------------------------------------------------

lg.info("read data : from: {}".format(conf.PATH_ERROR_MSG))
ERR  = prepare.server_data(source=conf.PATH_ERROR_MSG)
lg.info("read data : from: {}".format(conf.PATH_APP_INFO))
APP_INFO = prepare.server_data(source=conf.PATH_APP_INFO)

lg.info("read conf.: APP_ROUTER_INFO")
router_info = conf.APP_ROUTER_INFO

lg.info("arrange   : tags_metadata")
tags_metadata = []
for name, data in router_info.items():
    if data["use"]:
        data["name"] = name
        tags_metadata.append(data)
# tags_metadata = [data for name, data in router_info.items() if data["use"]]

lg.info("init.     : server = FastAPI - using configuration and text data")

server = FastAPI()

app = FastAPI(
    openapi_tags=tags_metadata,
    title=APP_INFO["proj_name"],
    version=APP_INFO["version"],
    summary=APP_INFO["summary"],
    description=APP_INFO["description"],
    contact={"name": "SmartHomeMyCastle",
             "email": "szillerke@gmail.com"},
    terms_of_service=APP_INFO["terms"],
    openapi_url=APP_INFO["url"].format(APP_INFO["proj_nick"])
    )

server.mount(path="/app", app=app, name="shmc")

# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   ENDED   -
# -------------------------------------------------------------------------------------------------------

# ATTENTION: mounting StaticFiles over the path you use for your server, will mess up your routing-paths,
# and "details: not found" message will indicate, you're routing is wrong."

# path: sets the string you must type into the browser, when accessing data. You may want to "act" asif it was in a
# subdirectory, where it isn't, or show the actual subdirectory if necessary.
# by entering "/", you ensure the browser finds it under: host:0000/... directly
# app contains the 'directory' parameter, which must have the actual subdirectory as an argument
# if you call your basic page 'index.html' it can be accessed directly, without entering the actual filename

server.mount(path="/", app=StaticFiles(directory="public", html=True), name="public")
# http://127.0.0.1:8000

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
            lg.debug("initiating: <router> from {}".format(os.path.basename(__file__)))
            router_instance = router_class()
            # we set arguments for the instance:
            if "arguments" in data and data["arguments"]:
                for param, arg in data["arguments"].items():
                    setattr(router_instance, param, arg)
                    lg.info("set router: {} - attributes set".format([name], data["prefix"]))
            # collect instances under their names:
            ROUTER_OBJECTS[name] = router_instance
            lg.info("add router: {} as {}.router() - under {}".format([name], data["module"], data["prefix"]))
            # add router instances to the <app> sub-server:
            app.include_router(router=router_instance, tags=[name], prefix=data["prefix"])
            lg.info("incl.rout.: {}".format(router_instance))
        except (ImportError, AttributeError):
            msg = ERR[103][LNG].format(name)
            lg.error(msg)
lg.debug("SUMMARY   : --------------------------------------------------------------------------------")
lg.debug("listing   : all routers included in <app> sub-server:")
for k, v in ROUTER_OBJECTS.items():
    lg.debug("      >>> :{:>12}: {}".format(k, v))


# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------

"""

"""

if __name__ == "__main__":
    import uvicorn
    # <server> is the parent scope. You need to run <server> It includes "/" path to serve Static Pages
    uvicorn.run("Server_SmartHomeMyCastle:server", host="127.0.0.1", port=12340, reload=True, log_level="debug")
