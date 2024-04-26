"""
This is an umbrella server application for the MHMC project. It uses different routers, that neew to be installed
 alongside the server in <shmc_routers>.
This server setup can be used for any collection / combination of routers it the MHMC project.
USE THIS API as entry point whether on an umbrella router or on local terminals.

<shmc_routers> is both a locally kept package for development reasons and also an installable package. 

FastAPI hints:
- Typing is absolutely necessary in python
- main scope: initiate global Processes and Objects here
"""

import logging
import importlib
# from pydantic import BaseModel as BaMo

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter

from shmc_server import server_preparation as prepare
import config as conf

# from SmartHomeEngine import SmartHomeEngine as Engine

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

# prepare.fsh()

lg.info("prepare   : Actions taken for {} version.".format({True: "LIVE", False: " DEV"}[conf.isLIVE]))


# -------------------------------------------------------------------------------------------------------
# -                                                                                 ENDED              -
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   START   -
# -------------------------------------------------------------------------------------------------------

lg.info("read data : from: {}".format(conf.PATH_ERROR_MSG))
ERROR_DATA  = prepare.server_data(source=conf.PATH_ERROR_MSG)
lg.info("read data : from: {}".format(conf.PATH_SERVER_INFO))
SERVER_INFO = prepare.server_data(source=conf.PATH_SERVER_INFO)

lg.info("read conf.: ROUTER_INFO")
router_info = conf.ROUTER_INFO

lg.info("arrange   : tags_metadata")
tags_metadata = [_ for _ in router_info if _["use"]]

lg.info("init.     : server = FastAPI - using configuration and text data")
server = FastAPI(
    openapi_tags=tags_metadata,
    title=SERVER_INFO["proj_name"],
    version=SERVER_INFO["version"],
    summary=SERVER_INFO["summary"],
    description=SERVER_INFO["description"],
    contact={"name": "SmartHomeMyCastle",
             "email": "szillerke@gmail.com"},
    terms_of_service=SERVER_INFO["terms"],
    openapi_url=SERVER_INFO["url"].format(SERVER_INFO["proj_nick"])
    )

router = APIRouter()

# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   ENDED   -
# -------------------------------------------------------------------------------------------------------

# path: sets the string you must type into the browser, when accessing data. You may want to "act" asif it was in a
# subdirectory, where it isn't, or show the actual subdirectory if necessary.
# by entering "/", you ensure the browser finds it under: host:0000/... directly
# app contains the 'directory' parameter, which must have the actual subdirectory as an argument
# if you call your basic page 'index.html' it can be accessed directly, without entering the actual filename

server.mount(path="/", app=StaticFiles(directory="shmc_public", html=True), name="documentation")
# http://127.0.0.1:8000

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   START   -
# -------------------------------------------------------------------------------------------------------------------

for _ in router_info:  # looping through routing_info as key, value
    if _['use']:
        # using an internal rule of our development:
        # routers are defined under the name: <name>_router in the router files.
        router_name = _['name'] + "_router"
        try:
            # from the module we import <name>.py files.
            # Py-file names are the keys of the <router_info> dictionary as well.
            router_obj = getattr(importlib.import_module(_['module']), router_name)  # fastapi.router.APIRouter() inst.
            server.include_router(router_obj, tags=[_['name']], prefix=_["prefix"])
            lg.info("router    : added '{}' with prefix {}".format(_['name'], _["prefix"]))
        except (ImportError, AttributeError):
            msg = "router    : could not find '{}'".format(_['name'])
            lg.error(msg)
            # raise Exception(msg)
        # we add the current router instance to our server: (using tags and prefixes)
        

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------

"""
== Install framework
This should be installed on the system itself, NOT only in virtual environment.
However: If you use it from venv, and want to have it in the venv, you can install it into the venv!

 pip install "fastapi[all]"

== Run server
If you want to run the server in venv: Switch to local virtual environment! Then...
Run the server allowing reload on changes, either from a terminal:

 source ./venv/bin/activate
 uvicorn Server_SmartHomeMyCastle:server --reload

or directly as a python code as shown in the __name__ clause below.

== Swagger
Use Swagger simplified Frontend to demo, test and dev-use your Endpoints:

 http://127.0.0.1:8000/docs
 http://127.0.0.1:8000/redoc

== Online

testtoken:

 https://auth.chain-recorder.com 
token example:
{"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJkWk4yeG1WU0d5Q3VDT251QlNFVzlUem1WbVRjWWNWc1Z1RWQwc1hGeWEwIn0.eyJleHAiOjE2OTI3MjI4MzIsImlhdCI6MTY5MjcyMjUzMiwianRpIjoiYTlmNGExMmYtZWNmYi00NmQ4LTk4NzEtN2NiODdiN2UxNWYxIiwiaXNzIjoiaHR0cDovLzE0My4xOTguMTQzLjIyNDo4MDgwL3JlYWxtcy9jaGFpbi1yZWNvcmRlciIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJjNTNkZjg2Ny1jZDAzLTRjNzMtYTA5Zi1jYmZiNWYzYjQzMTkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjaGFpbi1yZWNvcmRlciIsInNlc3Npb25fc3RhdGUiOiIwY2U5MzE2YS0yNDA3LTQ1ZjAtOTg0OC02ZjkyYzkwZDRhM2QiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vbG9jYWxob3N0LyoiLCIqLS1jaGFpbnJlY29yZGVyLm5ldGxpZnkuYXBwLyoiLCIqLmNoYWlucmVjb3JkZXIuY29tLyoiLCJodHRwOi8vMTI3LjAuMC4xOjgwMDAvKiIsImh0dHA6Ly9sb2NhbGhvc3QvKiIsImh0dHA6Ly8xMjcuMC4wLjEvKiIsImh0dHBzOi8vMTI3LjAuMC4xLyoiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIjI1NSIsIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1jaGFpbi1yZWNvcmRlciIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJlbWFpbCBwcm9maWxlIiwic2lkIjoiMGNlOTMxNmEtMjQwNy00NWYwLTk4NDgtNmY5MmM5MGQ0YTNkIiwiYXV0aG9yaXphdGlvbiI6WyIyNTUiXSwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJCcmFkbGV5IEZyZWVkb20iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJicmFkQHRoZWZyZWVkb21wZW9wbGUub3JnIiwiZ2l2ZW5fbmFtZSI6IkJyYWRsZXkiLCJmYW1pbHlfbmFtZSI6IkZyZWVkb20iLCJlbWFpbCI6ImJyYWRAdGhlZnJlZWRvbXBlb3BsZS5vcmcifQ.Ef37k5sbzjxLc7Ek3aRJq4r_nvm5Byn7h2RAra0Rf-zPbIp-ZON2Kllhsnh2UxpFQrHlwnTKX_fy_t1pCc_rXucM58oxtG0gTjFyilr5IkNNiM0x_vigLdViFtak3kILkq27TGWzMxg9hxp5JKVNTkaTJGuC4YHPfAwPD0Tt0q4","expires_in":300,"refresh_expires_in":1800,"refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJjZDBmZTNhYy0yNGM3LTQzOGQtOGQ0Ni1jNThlNGI1MTdhNTEifQ.eyJleHAiOjE2OTI3MjQzMzIsImlhdCI6MTY5MjcyMjUzMiwianRpIjoiMjAxOTFmNmYtOGM5ZC00NDRhLWJmYWEtMGMzNGRhMGVhYmRmIiwiaXNzIjoiaHR0cDovLzE0My4xOTguMTQzLjIyNDo4MDgwL3JlYWxtcy9jaGFpbi1yZWNvcmRlciIsImF1ZCI6Imh0dHA6Ly8xNDMuMTk4LjE0My4yMjQ6ODA4MC9yZWFsbXMvY2hhaW4tcmVjb3JkZXIiLCJzdWIiOiJjNTNkZjg2Ny1jZDAzLTRjNzMtYTA5Zi1jYmZiNWYzYjQzMTkiLCJ0eXAiOiJSZWZyZXNoIiwiYXpwIjoiY2hhaW4tcmVjb3JkZXIiLCJzZXNzaW9uX3N0YXRlIjoiMGNlOTMxNmEtMjQwNy00NWYwLTk4NDgtNmY5MmM5MGQ0YTNkIiwic2NvcGUiOiJlbWFpbCBwcm9maWxlIiwic2lkIjoiMGNlOTMxNmEtMjQwNy00NWYwLTk4NDgtNmY5MmM5MGQ0YTNkIn0.hAQYOJjG-0LyvZKEqVR6XF0bgyjOIs4LyxY1IG_Ou90","token_type":"Bearer","not-before-policy":0,"session_state":"0ce9316a-2407-45f0-9848-6f92c90d4a3d","scope":"email profile"}

CORS needed to be added to the browser
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Server_SmartHomeMyCastle:server", host="127.0.0.1", port=8000, reload=True, log_level="debug")
