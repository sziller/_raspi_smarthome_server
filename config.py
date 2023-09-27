isLIVE = True
isDIRECT_SETUP = True
API_SCOPE = "aquaponics"

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
     "module": "routers.aquaponics",
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
