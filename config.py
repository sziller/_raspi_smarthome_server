isLIVE = True
isDIRECT_SETUP = False

NECESSARY_DIRECTORIES = ["./images", "./documentation", "./documents", "./log"]

IP_AQUAPONIA = '10.3.77.1'

WAIT_SERVER = 3
HEARTBEAT_SERVER = 1

IS_PROCESS_RUNNING = True

PATH_ERROR_MSG = "./xdata/error.yaml"

ROUTER_INFO = router_info = [
    {"name": 'wallet',
     "use": False,
     "prefix": "/wllt",
     "ip4": '10.3.77.xx',
     "module": "routers.wallet",
     "description": "Information regarding SmartHome setup's BiTCoin wallet",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}},
    {"name": 'aquaponics',
     "use": True,
     "prefix": "/aqua",
     "ip4": '10.3.77.xx',
     "module": "mhmc_routers.aquaponics",
     "description": "Information regarding SmartHome setup's Aquaponic system",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}},
    {"name": "observatory",
     "use": False,
     "prefix": "/obsr",
     "ip": '10.3.77.xx',
     'module': "routers.observatory",
     "description": "Information regarding SmartHome setup's Observatory hub",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}
     },
    {"name": "room_01",
     "use": False,
     "prefix": "/r_01",
     "ip": '10.3.77.xx',
     'module': "routers.room_01",
     "description": "Information regarding SmartHome setup's Room_01 general manager",
     "externalDocs": {
         "description": "find additional info under: sziller.eu",
         "url": "http://sziller.eu"}}
               ]

# DATABASE related parameters:                                                          DB related - START
DATABASE_NAME           = "./.DB_MyHomeMyCastle.db"
DATABASE_STYLE          = "SQLite"
DB_ID_TABLE_IPS         = "restrictedips"
DB_ID_TABLE_USERS       = "users"
DB_ID_TABLE_DOCUMENTS   = "documents"
DB_ID_TABLE_SCHEDULED   = "scheduledtasks"
# DATABASE related parameters:                                                          DB related - ENDED

DEFAULT_USER_LIST       = [
    # 32char (128bit) hex-string representation of the UUID: double sha256 of the first email-address-string
    {   # "uuid": 'be7c2ca8de16d871c44bd9d1ef2d0df9',  # is generated once user's email is processed
        # "uuid": "0163977a-4c17-4caa-9db4-334de7aadf1b",
        "uuid": "aa",  # uuid - self generated
        "usr_ln": 'Ladanyi',
        "usr_fn": 'Sziller',
        "pubkey": None,
        "email_list": 'szillerke@gmail.com',  # last email is the actual one [-1]
        "timestamp": 0.0,  # is added when user hits DB
        "authorization": 15},  # binary sum - 11111111 - fully authorized - TBD
    {   "uuid": "bb",  # uuid - self generated
        "usr_ln": 'Ladanyi-Molnar',
        "usr_fn": 'Terez',
        "pubkey": None,
        "email_list": 'mterez@gmail.com',  # last email is the actual one [-1]
        "timestamp": 0.0,
        "authorization": 3}
    ]
