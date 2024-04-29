"""=== Public config file ==========================================================
Including settings for the Project, to be changed on or after install.
Not including sensitive data
================================================================== by Sziller ==="""
# Development settings:
isLIVE: bool                = True

# Language settings:
LANGUAGE_CODE = "EN"  # ["HU", "DE"]

# Path settings:
PATH_ROOT: str                  = "."
PATH_ERROR_MSG: str             = "{}/xdata/error.yaml"
PATH_APP_INFO: str              = "{}/xdata/shmc.yaml"

NECESSARY_DIRECTORIES: list     = ["./images", "./documentation", "./documents", "./log"]

# Log settings:
LOG_FORMAT: str                 = "%(asctime)s [%(levelname)8s]: %(message)s"
LOG_LEVEL: str                  = "DEBUG"  # NOTSET=0, DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
LOG_FILENAME: str               = "{}/log/srvr-shmc{}.log"  # location of logfile. 1st {} = ROOT_PATH, 2nd {} timestamp
LOG_TIMED: bool                 = True  # True: new log file created - stamp in name, False: no stamp, file overwritten
LOG_TIMEFORMAT: str             = "%y%m%d %H:%M:%S"

# DB settings:
DB_SESSION_NAME: str            = ".SmartHomeMyCastle.db"

'''
Routers receive the following parameters passed on startup:
{
    <name>:                               # name of the router - key
        {   "use": bool,                       # if current router instance is used
            "prefix": str,                     # path prefix for current router
            "ip": str[xx.xx.xx.xx],            # ip address
            "zmq_port": int,                   # if socket comm. allowed to engine, use this port
            "arguments": {},                   # dict of {param: arg} pairs for current router instance
            "module": str ["xxx.xxx"],         # module out of which "router" obj is instantiated
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
        "ip": '10.xx.xx.xx',
        "zmq_port": 0,
        "arguments": {},
        "module": "shmc_routers.WalletRouter_class",
        "description": "Information regarding SmartHome setup's BiTCoin wallet",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "aquaponics": {
        "use": True,
        "prefix": "/aqua",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52008,
        "arguments": {"nr_of_fish": 10000},
        "module": "shmc_routers.AquaRouter_class",
        "description": "Information regarding SmartHome setup's Aquaponic system",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "observatory": {
        "use": True,
        "prefix": "/obsr",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52902,
        "module": "shmc_routers.ObsrRouter_class",
        "description": "Information regarding SmartHome setup's Observatory hub",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "livingroom": {
        "use": True,
        "prefix": "/r_lv",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52903,
        "module": "shmc_routers.RoomRouter_class",  # probably 'room' only!
        "description": "Information regarding SmartHome setup's Room general manager",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "kidsroom": {
        "use": True,
        "prefix": "/r_ks",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52903,
        "module": "shmc_routers.RoomRouter_class",  # probably 'room' only!
        "description": "Information regarding SmartHome setup's Room general manager",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "bathroom": {
        "use": True,
        "prefix": "/r_ba",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52903,
        "module": "shmc_routers.RoomRouter_class",  # probably 'room' only!
        "description": "Information regarding SmartHome setup's Room general manager",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}}
    }

# DATABASE related parameters:                                                          DB related - START
DATABASE_NAME           = "./.DB_SmartHomeMyCastle.db"
DATABASE_STYLE          = "SQLite"
DB_ID_TABLE_IPS         = "restrictedips"
DB_ID_TABLE_USERS       = "users"
DB_ID_TABLE_DOCUMENTS   = "documents"
DB_ID_TABLE_SCHEDULED   = "scheduledtasks"
# DATABASE related parameters:                                                          DB related - ENDED

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
