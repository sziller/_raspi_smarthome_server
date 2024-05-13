"""=== Public config file ==========================================================
Including settings for the Project, to be changed on or after install.
Not including sensitive data
================================================================== by Sziller ==="""
import os

HOME = os.path.expanduser("~")  # experimental row to be developed later

# Development settings:
isLIVE: bool                = True

# Language settings:
LANGUAGE_CODE = "EN"  # ["HU", "DE"]

# Path settings:
PATH_ROOT: str                  = "."
PATH_ERROR_MSG: str             = "{}/xdata/error.yaml"
PATH_APP_INFO: str              = "{}/xdata/shmc.yaml"
PATH_STATIC_FROM: str           = "public"
PATH_STATIC_TO: str             = "/"

NECESSARY_DIRECTORIES: list     = ["./images", "./documentation", "./documents", "./log"]

# Log settings:
LOG_FORMAT: str                 = "%(asctime)s [%(levelname)8s]: %(message)s"
LOG_LEVEL: str                  = "DEBUG"  # NOTSET=0, DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
LOG_FILENAME: str               = "{}/log/srvr-shmc{}.log"  # location of logfile. 1st {} = ROOT_PATH, 2nd {} timestamp
LOG_TIMED: bool                 = False  # True: new log file created - stamp in name, False: no stamp, file overwritten
LOG_TIMEFORMAT: str             = "%y%m%d %H:%M:%S"

'''
Routers receive the following parameters passed on startup:
{
    <name>:                                    # name of the router - key
        {   "use": bool,                       # if current router instance is used
            "prefix": str,                     # path prefix for current router
            "arguments": {
                        "ip": str[xx.xx.xx.xx],     # ip address
                        "port": int,                # Engine's DB access port
                        "zmq_port": int,            # if socket comm. allowed to engine, use this port
            },                                  # dict of {param: arg} pairs for current router instance
            "module": str ["xxx.xxx"],          # module out of which "router" obj is instantiated
            "description": "Information regarding router",
                "externalDocs": {
                    "description": "find additional info under: sziller.eu",
                    "url": "http://sziller.eu"
            },
    <name-02>:
        {},
    ...     }
'''

# App settings:
APP_ID: str                     = "shmc"
APP_IS_PROCESS_RUNNING: bool    = True

# list necessary router data here:
APP_ROUTER_INFO = {
    'wallet': {
        "use": False,
        "prefix": "/wllt",
        "args": {"ip": '10.3.77.wlt',
                 "port": 8041,
                 "zmq_port": 0},
        "module": "shmc_routers.WalletRouter_class",
        "description": "Information regarding SmartHome setup's BiTCoin wallet",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "aquaponics": {
        "use": True,
        "prefix": "/aqua",
        "args": {"ip": '10.3.77.aqu',
                 "port": 8042,
                 "zmq_port": 52008},
        "module": "shmc_routers.AquaRouter_class",
        "description": "Information regarding SmartHome setup's Aquaponic system",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "observatory": {
        "use": True,
        "prefix": "/obsr",
        "args": {"ip": '10.3.77.36',
                 "port": 8043,
                 "zmq_port": 52902},
        "module": "shmc_routers.ObsrRouter_class",
        "description": "Information regarding SmartHome setup's Observatory hub",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "kidsroom": {
        "use": True,
        "prefix": "/r_ks",
        "args": {"ip": '10.3.77.42',
                 "port": 8050,
                 "zmq_port": 52903},
        "module": "shmc_routers.RoomRouter_class",  # probably 'room' only!
        "description": "Information regarding SmartHome setup's Room general manager",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "floroom": {
        "use": True,
        "prefix": "/r_lv",
        "args": {"ip": '10.3.77.36',
                 "port": 8051,
                 "zmq_port": 52903},
        "module": "shmc_routers.RoomRouter_class",  # probably 'room' only!
        "description": "Information regarding SmartHome setup's Room general manager",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    # "bathroom": {
    #     "use": True,
    #     "prefix": "/r_ba",
    #     "args": {"ip": '10.3.77.bth',
    #              "port": 8052,
    #              "zmq_port": 52903},
    #     "module": "shmc_routers.RoomRouter_class",  # probably 'room' only!
    #     "description": "Information regarding SmartHome setup's Room general manager",
    #     "externalDocs": {
    #         "description": "find additional info under: sziller.eu",
    #         "url": "http://sziller.eu"}}
    }

DEFAULT_USER_LIST       = [
    # 32char (128bit) hex-string representation of the UUID: double sha256 of the first email-address-string
    {   "uuid": "aa",  # uuid - self generated
        "usr_ln": 'Doe',
        "usr_fn": 'John',
        "pubkey": None,
        "email_list": 'JD@gmail.com',  # last email is the actual one [-1]
        "timestamp": 0.0,  # is added when user hits DB
        "authorization": 15},  # binary sum - 11111111 - fully authorized - TBD
    ]
