#!/home/sziller/Projects/901_RasPi_SmartHomeServer/_raspi_smarthome_server/venv/bin/python

"""=== App-interface to start SmartHomeMyCastle Server =======================================
Call this python script as:
python3 App_Server_inst.py
============================================================================ by Sziller ==="""

import os
import inspect
import logging
import config as conf
from dotenv import load_dotenv
from time_format import TimeFormat as TiFo
from shmc_server import ShmcServer


def app_server(**data_passed):
    """=== Function name: app_server ===================================================================================
    Use this code to run the SHMC server!
    ============================================================================================== by Sziller ==="""
    cfn = inspect.currentframe().f_code.co_name  # current class name
    lg.info("START: {:>85} <<<".format(cfn))
    lg.warning("          : ======================================")
    lg.warning({True: "          : =            LIVE SESSION            =",
                False: "          : =            DEV  SESSION            ="}[conf.isLIVE])
    lg.warning("          : ={:^36}=".format(__name__))
    lg.info("          : =         user languange: {}         =".format(data_passed["lng"]))
    lg.warning("          : ======================================")
    server = ShmcServer.Server()
    for param, arg in data_passed.items():
        setattr(server, param, arg)
        print("param: {:>20} : {}".format(param, getattr(server, param)))
    server.process()
    server.serve_forever()
    pass


if __name__ == "__main__":
    # READ BASIC SETTINGS                                                                   -   START   -
    # from .env:
    load_dotenv()
    # <server> is the parent scope. You need to run <server> It includes "/" path to serve Static Pages
    # do not define logger info!

    # log settings:
    log_format = conf.LOG_FORMAT
    log_level = getattr(logging, conf.LOG_LEVEL)
    log_ts = "_{}".format(TiFo.timestamp()) if conf.LOG_TIMED else ""
    log_tf = conf.LOG_TIMEFORMAT
    root_path = conf.PATH_ROOT
    log_path = conf.LOG_PATH.format(root_path)
    log_fullfilename = conf.LOG_FILENAME.format(log_path, log_ts)
    
    # Setting up logger                                                                     -   START   -
    if not os.path.exists(log_path): os.mkdir(log_path)
    lg = logging.getLogger("shmc")
    # Using config.py data - configurate logger:
    logging.basicConfig(filename=log_fullfilename,
                        level=log_level,
                        format=log_format,
                        datefmt=log_tf,
                        filemode="w")
    # initial messages
    lg.warning("FILE: {:>86} <<<".format(__file__))
    lg.warning("LOGGER namespace: {:>74} <<<".format(__name__))
    lg.debug("listing   : config settings:")
    for k, v in {param: arg for param, arg in vars(conf).items() if not param.startswith('__')}.items():
        lg.debug("{:>20}: {}".format(k, v))
    # Setting up logger                                                                     -   ENDED   -

    kwargs_server = {
        "srv_ip": os.getenv("SRV_IP"),
        "srv_port": int(os.getenv("SRV_PORT")),
        "session_name_shmc": os.getenv("DB_FULLNAME_SHMC"),
        "session_style_shmc": os.getenv("DB_STYLE_SHMC"),
        "session_name_auth": os.getenv("DB_FULLNAME_AUTH"),
        "session_style_auth": os.getenv("DB_STYLE_AUTH"),
        "lng": conf.LANGUAGE_CODE,
        "fsh_dir_info": conf.NECESSARY_DIRECTORIES,
        "root_path": conf.PATH_ROOT,
        "err_msg_path": conf.PATH_ERROR_MSG.format(conf.PATH_ROOT),
        "app_inf_path": conf.PATH_APP_INFO.format(conf.PATH_ROOT),
        "mount_from": conf.PATH_STATIC_FROM,
        "mount_to": conf.PATH_STATIC_TO,
        "router_info": conf.APP_ROUTER_INFO
        }
    
    app_server(**kwargs_server)
    

