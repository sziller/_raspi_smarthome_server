"""
FastAPI hints:
- Typing is absolutely necessary in python
- main scope: initiate global Processes and Objects here
"""

import os
import json
import time
import urllib
import yaml
import inspect
import multiprocessing
from multiprocessing import Process
# from pydantic import BaseModel as BaMo
from typing import Optional, Dict, cast, Any

from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

# import server_preparation as prepare
import config as cnf
# from SmartHomeEngine import SmartHomeEngine as Engine

print("========================")
print({True: "=     LIVE SESSION     =", False: "=     DEV  SESSION     ="}[cnf.isLIVE])
print("={:^22}=".format(__name__))
print("========================")

# -------------------------------------------------------------------------------------------------------
# - Basic setup                                                                      START              -
# -------------------------------------------------------------------------------------------------------

# prepare.fsh()

print("[PREPARE]: Actions taken for {} version:".format({True: "LIVE", False: " DEV"}[cnf.isLIVE]))


# -------------------------------------------------------------------------------------------------------
# -                                                                                 ENDED              -
# -------------------------------------------------------------------------------------------------------

router_info = {'aquaponics': {'use': True, "prefix": "/aqu0"},
               'observatory': {'use': True, 'prefix': "/obsr"},
               'room': {'use': True, "prefix": "/room_01"}
               }


# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   START   -
# -------------------------------------------------------------------------------------------------------
tags_metadata = [
    
    {"name": "Aquaponics",
     "description": "Information regarding SmartHome setup's Aquaponic system",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}
     },
    {"name": "Observatory",
     "description": "Information regarding SmartHome setup's Observatory hub",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}
     },
    {"name": "Room_01",
     "description": "Information regarding SmartHome setup's Room_01 general manager",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}
     }
]

summary = """
This is an open project to be shipped someday.
"""
description = """
## SmartHome with no chains attached
****
Why My Home My Castle?
Well... we kinda all know that, don't we?
MHMC lets you and keeps you in the drivers seat.
****

## Install
coming soon...

## About
sziller.eu
"""

fill_in = {"path": cnf.PATH_ERROR_MSG, "fn": "Server_SmartHome.py"}
with open(cnf.PATH_ERROR_MSG, 'r') as stream:
    try:
        parsed_yaml = yaml.safe_load(stream)
        ERROR = parsed_yaml
        print("Loaded error messages from {path} - sais {fn}".format(**fill_in))
    except yaml.YAMLError as exc:
        print(exc)
        print("Failed to load error messages from {path} - sais {fn}".format(**fill_in))

server = FastAPI(
    openapi_tags=tags_metadata,
    title="my Home my Castle",
    version="v0.0.0",
    summary=summary,
    description=description,
    contact={"name": "MyHomeMyCastle",
             "email": "szillerke@gmail.com"},
    terms_of_service="",
    openapi_url="/api/v0/MyHomeMyCastle.json"
    )

router = APIRouter()



# -------------------------------------------------------------------------------------------------------
# Server application                                                                        -   ENDED   -
# -------------------------------------------------------------------------------------------------------

server.mount("/documentation", StaticFiles(directory="documentation", html=True), name="documentation")

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   START   -
# -------------------------------------------------------------------------------------------------------------------

# from auth import jwt_bearer as jwtb
# @server.get("/v1/jwt_study", tags=["Supa vs. KeyCloak"])
# async def GET_jwt_details(current_user: dict = Depends(jwtb.JwtBearer())):
#     return {"answer": current_user}

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                            Engine records -   START   -
# -------------------------------------------------------------------------------------------------------------------

from routers.observatory import observatory_router
from routers.aquaponics import aquaponics_router
from routers.room_01 import room01_router

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------

server.include_router(observatory_router, prefix="/obs", tags=["Observatory"])
server.include_router(aquaponics_router, prefix="/aqu", tags=["Aquaponics"])
server.include_router(room01_router, prefix="/r01", tags=["Room_01"])

"""
== Install framework
This should be installed on the system itself, NOT only in virtual environment.
However: If you use it from venv, and want to have it in the venv, you can install it into the venv!

 pip install "fastapi[all]"

== Run server
If you want to run the server in venv: Switch to local virtual environment! Then...
Run the server allowing reload on changes:

 source ./venv/bin/activate 
 uvicorn Server_SmartHome:server --reload

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

