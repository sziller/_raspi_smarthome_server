isLIVE = True
isDIRECT_SETUP = False

NECESSARY_DIRECTORIES = ["./images", "./documentation", "./documents", "./log"]

WAIT_SERVER = 3
HEARTBEAT_SERVER = 1

IS_PROCESS_RUNNING = True

PATH_ERROR_MSG = "./xdata/error.yaml"
PATH_SERVER_INFO = "./xdata/shmc.yaml"

# list necessary router data here:
ROUTER_INFO = router_info = [
    {"name": 'wallet',
     "use": False,
     "prefix": "/wllt",
     "ip": '10.xx.xx.xx',
     "zmq_port": 0,
     "module": "shmc_routers.wallet",
     "description": "Information regarding SmartHome setup's BiTCoin wallet",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}},
    {"name": 'aquaponics',
     "use": True,
     "prefix": "/aqua",
     "ip": '10.xx.xx.xx',
     "zmq_port": 52008,
     "module": "shmc_routers.aquaponics",
     "description": "Information regarding SmartHome setup's Aquaponic system",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}},
    {"name": "observatory",
     "use": True,
     "prefix": "/obsr",
     "ip": '10.xx.xx.xx',
     "zmq_port": 52902,
     'module': "shmc_routers.observatory",
     "description": "Information regarding SmartHome setup's Observatory hub",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}
     },
    {"name": "room",
     "use": True,
     "prefix": "/r_{}",
     "ip": '10.xx.xx.xx',
     "zmq_port": 52903,
     'module': "shmc_routers.room",  # probably 'room' only!
     "description": "Information regarding SmartHome setup's Room_01 general manager",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}}
               ]

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
