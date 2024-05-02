import time
import logging
import inspect
from shmc_routers._ShmcBaseRouter import ShmcBaseRouter
from shmc_messages import msg
from shmc_messages import msg_aqua

IS_PROCESS_RUNNING = True

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -


class AquaRouter(ShmcBaseRouter):
    """Class name: AquaponicsRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name
    
    def __init__(self, name, alias, ip: str = "0.0.0.0", port: int = 0, db_fullname=None, db_style=None):
        super().__init__(name, alias, ip, port, db_fullname, db_style)
        lg.debug("initiated : '{}' router as object {}".format(self.name, self.ccn))
        self.IS_PROCESS_RUNNING = True
        
        self.add_api_route("/v0/system-main-switch-state/",     self.GET_system_main_switch_state,  methods=["GET"])
        self.add_api_route("/v0/actual-state",                  self.GET_actual_state,              methods=["GET"])
        self.add_api_route("/v0/command-engine-ON/{message}",   self.POST_command_engine_on,        methods=["POST"])
        self.add_api_route("/v0/command-engine-OFF/{message}",  self.POST_command_engine_off,       methods=["POST"])
        self.add_api_route("/v0/happening-data/{style}",        self.GET_happening_data,            methods=["GET"])
        self.add_api_route("/v0/settings-data/{category}",      self.GET_settings_data,             methods=["GET"])
        self.add_api_route("/v0/timed-happening",               self.PUT_timed_happening,           methods=["PUT"])
        self.add_api_route("/v0/instant-event",                 self.POST_instant_event,            methods=["POST"])
        self.add_api_route("/v0/timed-happening",               self.DELETE_timed_happening,        methods=["DELETE"])
    
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------
    async def GET_system_main_switch_state(self):
        """=== Function name: GET_system_main_switch_state =============================================================
        description...\n
        ========================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
    
        if self.IS_PROCESS_RUNNING:
            return True
        else:
            return False

    async def GET_actual_state(self):
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
                                           message="OK - sais {} - {}".format(cmn, self.nr_of_fish),
                                           timestamp=timestamp)
        return response.as_dict()

    async def POST_command_engine_on(self, message: str = "", hcdd: dict or None = None):
        """=== Function name: POST_command_engine_on =======================================================================
        Starting the Aquaponic system. Actual physical Details to be checked!
        :param message: str - text to be processed on the Backend
        :param hcdd: dict - HardCodedDDefaultData
         ============================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        if not self.IS_PROCESS_RUNNING:
            self.IS_PROCESS_RUNNING = True
            print("ENGINE is running")
        else:
            print("An ENGINE instance is already running, second one was NOT instantiated!")
        return True

    async def POST_command_engine_off(self, message: str = ""):
        """=== Function name: POST_command_engine_on =======================================================================
        Shuting off the Aquaponic system. Actual physical Details to be checked!
        :param message: str - text to be processed on the Backend
         ============================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        if self.IS_PROCESS_RUNNING:
            print("TERMINATING ENGINE as background process...")
            self.IS_PROCESS_RUNNING = False
            print("ENGINE stopped")
        else:
            print("No ENGINE instance was running so far, NOTHING happened!")
        return False

    async def GET_happening_data(self, style: str):
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

    async def GET_settings_data(self, category: str):
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

    async def PUT_timed_happening(self, style: str, act: str, timing: list[dict]):
        """=== Function name: PUT_timed_happening ======================================================================
        description...
    
        :param timing: list - list of timecodes, format according to <style> picked
        :param act: str     - the action to be added a timecode to.
                              e.g.: 'feeding', 'waterstream' 'light-2'
        :param style: str   - 'event' or 'process' depending on the dynamic of the happening:
                              'even' is a point in time
                              'process' is a duration
        ========================================================================================== by Sziller ==="""
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

    async def POST_instant_event(self, act: str):
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

    async def DELETE_timed_happening(self, style: str, act: str, timing: list[dict]):
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

'''
@router.post("/send-message")
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
'''
