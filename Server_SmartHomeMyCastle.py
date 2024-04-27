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

import logging
import importlib
# from pydantic import BaseModel as BaMo
from shmc_routers.aquaponics_router import aquaponics_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from shmc_server import server_preparation as prepare
import config as conf


# Setting up logger                                         logger                      -   START   -
lg = logging.getLogger()
logging.basicConfig(filename="./log/srvr_shmc.log", level=logging.NOTSET, filemode="w",
                    format="%(asctime)s [%(levelname)8s]: %(message)s", datefmt='%y%m%d %H:%M:%S')
# Setting up logger                                         logger                      -   ENDED   -

lg.warning("START: {:>85} <<<".format('__name__ == "__main__" namespace: Server_SmartHomeMyCastle.py'))
lg.warning("          : =========================")
lg.warning({True:  "          : =     LIVE  SESSION     =",
            False: "          : =      DEV SESSION      ="}[conf.isLIVE])
lg.warning("          : ={:^23}=".format(__name__))
lg.warning("          : =========================")

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
ERROR_DATA  = prepare.server_data(source=conf.PATH_ERROR_MSG)
lg.info("read data : from: {}".format(conf.PATH_APP_INFO))
APP_INFO = prepare.server_data(source=conf.PATH_APP_INFO)

lg.info("read conf.: APP_ROUTER_INFO")
router_info = conf.APP_ROUTER_INFO

lg.info("arrange   : tags_metadata")
tags_metadata = [_ for _ in router_info if _["use"]]

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


for _ in router_info:  # looping through routing_info as key, value
    if _['use']:
        # using an internal rule of our development:
        # routers are defined under the name: <name>_router in the router files.
        router_name = _['module'].split(sep=".")[1]
        try:
            # from the module we import <name>.py files.
            # Py-file names are the keys of the <router_info> dictionary as well.
            router_obj = getattr(importlib.import_module(_['module']), router_name)  # fastapi.router.APIRouter() inst.
            print("---------------------------")
            print(router_obj.nr_of_fish)
            router_obj.nr_of_fish = 77
            print(router_obj.nr_of_fish)
            print("---------------------------")
            tags_in = [_['name']]
            prefix_in = _["prefix"]
            app.include_router(router=router_obj, tags=tags_in, prefix=prefix_in)
            # lg.info("router_obj: {}\ntags_in   : {}\nprefix_in : {}".format(router_obj, tags_in, prefix_in))
            lg.info("incl.rout.: '{}' as {} - under {}".format(tags_in, router_obj, prefix_in))
        except (ImportError, AttributeError):
            msg = "router    : could not find '{}'".format(_['name'])
            lg.error(msg)
            # raise Exception(msg)
        # we add the current router instance to our app: (using tags and prefixes)

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
for k in server.router.routes:
    if k.name == "shmc":
        for x, y in k.app.router.__dict__.items():
            print("{}: {}".format(x, y))
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# for k, v in server.__dict__.items():
#     print("{}: {}".format(k, v))

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------

"""

"""

if __name__ == "__main__":
    import uvicorn
    # <server> is the parent scope. You need to run <server> It includes "/" path to serve Static Pages
    uvicorn.run("Server_SmartHomeMyCastle:server", host="127.0.0.1", port=12340, reload=True, log_level="debug")
