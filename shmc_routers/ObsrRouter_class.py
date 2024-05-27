import os
import zmq
import time
import logging
import inspect
from shmc_routers._ShmcBaseRouters import EngineMngrRouter
from shmc_routers._AuthPrimitives import *
from shmc_messages import msg

# Setting up logger                                                                     -   START   -
lg = logging.getLogger("shmc")
# Setting up logger                                                                     -   ENDED   -
    

class ObsrRouter(EngineMngrRouter):
    """Class name: RoomRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name

    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str                    = "0.0.0.0",
                 port: int                  = 0,
                 auth_dict: dict or None    = None,
                 db_fullname: str or None   = None,
                 db_style: str or None      = None,
                 zmq_port: int              = 0):
        super().__init__(name, alias, ip, port, auth_dict, db_fullname, db_style, zmq_port)
        lg.debug("initiated : '{}' router as object {}".format(self.name, self.ccn))

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
    
    async def GET_send_message(self, message: str, current_user: UserInDB = Depends(get_current_active_user)):
        """=== Function name: GET_send_message =========================================================================
        description...  
    
        :param message: str -  'pins' or 'process' depending on the dynamic of the happening:
                                'pin_info' is a point in time
                                'process' is a duration
        ============================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        required_auth_code: int = 3
        timestamp = time.time()
        lg.info("request   : {} / {:>25} says {} at {}".format(timestamp, cmn, self.ccn, os.path.basename(__file__)))
        if self.check_authorization(auth_code=current_user.auth_code, nth_switch=required_auth_code):
            data_dict = {"command": cmn,
                         "user_id": current_user.username,
                         "email": current_user.email,
                         "signature": b'',
                         "payload": {'message': message},
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
        else:
            lg.warning("prohibited: nr.{:>2} - says {} at {}"
                    .format(required_auth_code, cmn, self.ccn, os.path.basename(__file__)))
            credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                 detail="Current User cannot add/remove new Users!",
                                                 headers={"WWW-Authenticate": "Bearer"})
            raise credential_exception

    async def GET_photo(self, current_user: UserInDB = Depends(get_current_active_user)):
        """=== Function name: GET_photo ========================================================  
        Endpoint to create an image in Engine  
        ======================================================================= by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        required_auth_code: int = 5
        timestamp = time.time()
        lg.info("request   : {} / {:>25} says {} at {}".format(timestamp, cmn, self.ccn, os.path.basename(__file__)))
        if self.check_authorization(auth_code=current_user.auth_code, nth_switch=required_auth_code):
            lg.info("authorized: nr.{:>2} - says {} at {}"
                     .format(required_auth_code, cmn, self.ccn, os.path.basename(__file__)))
            data_dict = {"command": cmn,
                         "user_id": current_user.username,
                         "email": current_user.email,
                         "signature": b'',
                         "payload": {},
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
        else:
            lg.warning("prohibited: nr.{:>2} - says {} at {}"
                    .format(required_auth_code, cmn, self.ccn, os.path.basename(__file__)))
            credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                 detail="Current User cannot add/remove new Users!",
                                                 headers={"WWW-Authenticate": "Bearer"})
            raise credential_exception
        
        
        
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
    

