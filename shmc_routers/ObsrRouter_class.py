import os
import zmq
import time
import logging
import inspect
from shmc_routers._ShmcBaseRouter import ShmcBaseRouter
from shmc_routers.auth import *
from shmc_messages import msg

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -
    

class ObsrRouter(ShmcBaseRouter):
    """Class name: RoomRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name

    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str = "0.0.0.0",
                 port: int = 0,
                 zmq_port: int = 0,
                 db_fullname=None,
                 db_style=None):
        super().__init__(name, alias, ip, port, db_fullname, db_style)
        lg.debug("initiated : '{}' router as object {}".format(self.name, self.ccn))
        self.name: str                  = name
        self.alias: str                 = alias
        self.ip: str                    = ip            # ip of remote Engine and Message handler (zmq socket endpoint)
        self.port: int                  = port          # port remote server runs on - for DB communication
        self.zmq_port: int              = zmq_port      # port of remote Message handler (zmq socket endpoint)
        self.db_fullname: (str, None)   = db_fullname
        self.db_style: (str, None)      = db_style

        # list of default endpoints for all child Router class-objects                              -   START   -
        self.add_api_route(path="/v0/send-message/",
                           endpoint=self.GET_send_message,
                           response_model=msg.ExtRespMsg,
                           methods=["GET"])
        self.add_api_route(path="/v0/photo/",
                           endpoint=self.GET_photo,
                           response_model=msg.ExtRespMsg,
                           methods=["GET"])
        # list of default endpoints for all child Router class-objects                              -   ENDED   -

    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------
    
    async def GET_send_message(self, message: str):
        """=== Function name: GET_send_message =========================================================================
        description...  
    
        :param message: str -  'pins' or 'process' depending on the dynamic of the happening:
                                'pin_info' is a point in time
                                'process' is a duration
        ============================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        lg.debug("request   : {} / {:>25} says {} at {}".format(timestamp, cmn, self.ccn, os.path.basename(__file__)))
        data_dict = {"command": cmn,
                     "user_id": "sziller_dev",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {'message': message},
                     "timestamp": timestamp}
        # msg_router_to_engine = msg.IntMsg(**data_dict)
        msg_router_to_engine = msg.InternalMsg.init_by_dict(**data_dict)
        
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        lg.info("socket up : {}:{}".format(self.ip, self.zmq_port))
        socket.connect("tcp://{}:{}".format(self.ip, self.zmq_port))
        socket.send_pyobj(msg_router_to_engine)
        sock_response = socket.recv_pyobj()
        socket.close()  # Close the socket after use
        context.term()  # Terminate the ZeroMQ context
        return msg.ExtRespMsg(**sock_response.__dict__)

    async def GET_photo(self, current_user: UserInDB = Depends(get_current_active_user)):
        """=== Function name: GET_photo ========================================================  
        Endpoint to create an image in Engine  
        ======================================================================= by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        lg.debug("request   : {} / {:>25} says {} at {}".format(timestamp, cmn, self.ccn, os.path.basename(__file__)))
        print(current_user)
        data_dict = {"command": cmn,
                     "user_id": "sziller_dev",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {current_user.username},
                     "timestamp": timestamp}
        msg_router_to_engine = msg.InternalMsg.init_by_dict(**data_dict)
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        lg.info("socket up : {}:{}".format(self.ip, self.zmq_port))
        socket.connect("tcp://{}:{}".format(self.ip, self.zmq_port))
        socket.send_pyobj(msg_router_to_engine)
        sock_response = socket.recv_pyobj()

        socket.close()  # Close the socket after use
        context.term()  # Terminate the ZeroMQ context
        return msg.ExtRespMsg(**sock_response.__dict__)
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
    

