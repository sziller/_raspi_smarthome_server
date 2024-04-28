isLIVE = True
isDIRECT_SETUP = False

NECESSARY_DIRECTORIES = ["./images", "./documentation", "./documents", "./log"]

WAIT_SERVER = 3
HEARTBEAT_SERVER = 1

IS_PROCESS_RUNNING = True

PATH_ERROR_MSG = "./xdata/error.yaml"
PATH_APP_INFO = "./xdata/shmc.yaml"

# Routers receive the following parameters passed on startup:
# {
# <name>:                               # name of the router - key
#   {"use": bool,                       # if current router instance is used
#    "prefix": str,                     # path prefix for current router
#    "ip": str[xx.xx.xx.xx],            # ip address
#    "zmq_port": int,                   # if socket comm. allowed to engine, use this port
#    "arguments": {},                   # dict of {param: arg} pairs for current router instance
#    "module": str ["xxx.xxx"],         # module out of which "router" obj is instantiated
#      "description": "Information regarding router",
#      "externalDocs": {
#          "description": "find additional info under: sziller.eu",
#          "url": "http://sziller.eu"},
# <name-02>: {},
# <name-03>: {}
#          }

# list necessary router data here:
APP_ROUTER_INFO = {
    'wallet': {
        "use": False,
        "prefix": "/wllt",
        "ip": '10.xx.xx.xx',
        "zmq_port": 0,
        "arguments": {},
        "module": "shmc_routers.wallet_router",
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
        "module": "shmc_routers.aquaponics_router",
        "description": "Information regarding SmartHome setup's Aquaponic system",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "observatory": {
        "use": True,
        "prefix": "/obsr",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52902,
        "module": "shmc_routers.observatory_router",
        "description": "Information regarding SmartHome setup's Observatory hub",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "livingroom": {
        "use": True,
        "prefix": "/r_lv",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52903,
        "module": "shmc_routers.room_router",  # probably 'room' only!
        "description": "Information regarding SmartHome setup's Room general manager",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "kidsroom": {
        "use": True,
        "prefix": "/r_ks",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52903,
        "module": "shmc_routers.room_router",  # probably 'room' only!
        "description": "Information regarding SmartHome setup's Room general manager",
        "externalDocs": {
            "description": "find additional info under: sziller.eu",
            "url": "http://sziller.eu"}},
    "bathroom": {
        "use": True,
        "prefix": "/r_ba",
        "ip": '10.xx.xx.xx',
        "zmq_port": 52903,
        "module": "shmc_routers.room_router",  # probably 'room' only!
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
