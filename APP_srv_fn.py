#!/home/sziller/Projects/901_RasPi_SmartHomeServer/_raspi_smarthome_server/venv/bin/python

"""=== App-interface to start SmartHomeMyCastle Server =======================================
Call this python script as:
python3 APP_srv_fn.py
============================================================================ by Sziller ==="""

import os
import uvicorn
from dotenv import load_dotenv
from shmc_server import serverFunction_SHMC


if __name__ == "__main__":
    load_dotenv()
    # <server> is the parent scope. You need to run <server> It includes "/" path to serve Static Pages
    # do not define logger info!
    uvicorn.run(serverFunction_SHMC.server,    host=os.getenv("SRV_IP"), port=int(os.getenv("SRV_PORT")))
    
