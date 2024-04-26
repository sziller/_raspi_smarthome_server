import time

from fastapi import APIRouter
from dotenv import load_dotenv
import os
import inspect
import config as conf
import zmq
from shmc_msg import msg
from shmc_msg import msg_aqua

if conf.isDIRECT_SETUP:  # Direct outside connection: No Server in the network in front of this API towards Internet
    pass
else:  # Indirect outside connection: There IS a Server in the network - forwarding requests, processing answers
    pass

load_dotenv()
aquaponics_router = APIRouter()
process_engine = None


# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   START   -
# -------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------- Endpoints:      ON / OFF


@aquaponics_router.get("/v0/system-main-switch-state/")                     # GET: /v0/system-main-switch-state/
async def GET_system_main_switch_state():
    """=== Function name: GET_system_main_switch_state ===============================================================\n
    description...\n
    ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    if conf.IS_PROCESS_RUNNING:
        return True
    else:
        return False


@aquaponics_router.post("/v0/command-engine-ON/{message}")                  # POST: /v0/command-engine-ON/{message}
async def POST_command_engine_on(message: str = "", hcdd: dict or None = None):
    """=== Function name: POST_command_engine_on =======================================================================
    Starting the Aquaponic system. Actual physical Details to be checked!
    :param message: str - text to be processed on the Backend
    :param hcdd: dict - HardCodedDDefaultData
     ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    if not conf.IS_PROCESS_RUNNING:
        conf.IS_PROCESS_RUNNING = True
        print("ENGINE is running")
    else:
        print("An ENGINE instance is already running, second one was NOT instantiated!")
    return True


@aquaponics_router.post("/v0/command-engine-OFF/{message}")                           # POST: /v0/command-engine-OFF/{message}
async def POST_command_engine_off(message: str = ""):
    """=== Function name: POST_command_engine_on =======================================================================
    Shuting off the Aquaponic system. Actual physical Details to be checked!
    :param message: str - text to be processed on the Backend
     ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    if conf.IS_PROCESS_RUNNING:
        print("TERMINATING ENGINE as background process...")
        conf.IS_PROCESS_RUNNING = False
        print("ENGINE stopped")
    else:
        print("No ENGINE instance was running so far, NOTHING happened!")
    return False

# ----------------------------------------------------------------------------------------- Endpoints:      INFO


@aquaponics_router.get("/v0/actual-state")                                                            # GET: v0/actual-state
async def GET_actual_state():
    """=== Function name: GET_actual_state =============================================================================
    description...
    ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    data_dict = {"command": "GET_actual_state",
                 "user_id": "sziller_dev",
                 "email": "szillerke@gmail.com",
                 "signature": b'',
                 "payload": {},
                 "timestamp": timestamp}
    data = msg_aqua.SrvrToAquaRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()


@aquaponics_router.get("/v0/happening-data/{style}")                                          # GET: /v0/happening-data/{style}
async def GET_happening_data(style: str):
    """=== Function name: GET_happening_data ===========================================================================
    description...

    :param style: str - 'event' or 'process' depending on the dynamic of the happening:
                        'even' is a point in time
                        'process' is a duration
    ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    data_dict = {"command": "GET_happening_data",
                 "user_id": "sziller_dev",
                 "email": "szillerke@gmail.com",
                 "signature": b'',
                 "payload": {'style': style},
                 "timestamp": timestamp}
    data = msg_aqua.SrvrToAquaRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()


@aquaponics_router.get("/v0/settings-data/{category}")                                        # GET: /v0/settings-data/{category}
async def GET_settings_data(category: str):
    """=== Function name: GET_settings_data ===========================================================================
    description...

    :param category: str -  'pins' or 'process' depending on the dynamic of the happening:
                            'pin_info' is a point in time
                            'process' is a duration
    ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    data_dict = {"command": "GET_settings_data",
                 "user_id": "sziller_dev",
                 "email": "szillerke@gmail.com",
                 "signature": b'',
                 "payload": {'category': category},
                 "timestamp": timestamp}
    data = msg_aqua.SrvrToAquaRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()

# ----------------------------------------------------------------------------------------- Endpoints:      Control


@aquaponics_router.put("/v0/timed-happening")                                                     # PUT: /v0/timed-happening
async def PUT_timed_happening(style: str, act: str, timing: list[dict]):
    """=== Function name: PUT_timed_happening ==========================================================================
    description...

    :param timing: list - list of timecodes, format according to <style> picked
    :param act: str     - the action to be added a timecode to.
                          e.g.: 'feeding', 'waterstream' 'light-2'
    :param style: str   - 'event' or 'process' depending on the dynamic of the happening:
                          'even' is a point in time
                          'process' is a duration
    ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    data_dict = {"command": "PUT_timed_happening",
                 "user_id": "sziller_dev",
                 "email": "szillerke@gmail.com",
                 "signature": b'',
                 "payload": {'style': style, 'act': act, 'timing': timing},
                 "timestamp": timestamp}
    data = msg_aqua.SrvrToAquaRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()


@aquaponics_router.post("/v0/instant-event")                                                      # POST: /v0/instant-event
async def POST_instant_event(act: str):
    """=== Function name: POST_instant_event ===========================================================================
    description...

    :param act: str     - the action to be added a timecode to.
                          e.g.: 'feeding', 'waterstream' 'light-2'
     ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    data_dict = {"command": "POST_instant_event",
                 "user_id": "sziller_dev",
                 "email": "szillerke@gmail.com",
                 "signature": b'',
                 "payload": {'act': act},
                 "timestamp": timestamp}
    data = msg_aqua.SrvrToAquaRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()


@aquaponics_router.delete("/v0/timed-happening")                                                  # DELETE: /v0/timed-happening
async def DELETE_timed_happening(style: str, act: str, timing: list[dict]):
    """=== Function name: DELETE_timed_happening =======================================================================
    description...

    :param timing: list - list of timecodes, format according to <style> picked
    :param act: str     - the action to be added a timecode to.
                          e.g.: 'feeding', 'waterstream' 'light-2'
    :param style: str   - 'event' or 'process' depending on the dynamic of the happening:
                          'even' is a point in time
                          'process' is a duration
    ============================================================================================== by Sziller ==="""
    cmn = inspect.currentframe().f_code.co_name  # current method name
    timestamp = time.time()
    data_dict = {"command": "DELETE_timed_happening",
                 "user_id": "sziller_dev",
                 "email": "szillerke@gmail.com",
                 "signature": b'',
                 "payload": {'style': style, 'act': act, 'timing': timing},
                 "timestamp": timestamp}
    data = msg_aqua.SrvrToAquaRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()


@aquaponics_router.post("/send-message")
async def send_message(message: str):
    print("-----")
    print(os.getenv("ZMQ_PORT"))
    print("-----")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print("-----")
    print(os.getenv("ZMQ_PORT"))
    print("-----")
    socket.connect("tcp://localhost:{}".format(os.getenv("ZMQ_PORT")))
    socket.send_string(message)
    response = socket.recv_string()

    socket.close()  # Close the socket after use
    context.term()  # Terminate the ZeroMQ context
    return {"message": response}

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------
