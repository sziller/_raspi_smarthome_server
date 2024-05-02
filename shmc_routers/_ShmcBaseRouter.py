import time
import inspect
from fastapi import APIRouter
from shmc_messages import msg


class ShmcBaseRouter(APIRouter):
    """=== Class name: ShmcBaseRouter(APIRouter) =======================================================================
    Default Router parent class for the SHMC development. 
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name
    
    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str = "0.0.0.0",
                 port: int = 0,
                 db_fullname: (str, None) = None,
                 db_style: (str, None) = None
                 ):
        super().__init__()
        self.name: str              = name
        self.alias: str             = self.name[:4] if alias == "" else alias
        self.ip: str                = ip
        self.port: int              = port
        self.db_fullname: str       = db_fullname
        self.db_style: str          = db_style
    
        # list of default endpoints for all child Router class-objects                              -   START   -
        self.add_api_route("/v0/basic-config",                  self.GET_basic_config,              methods=["GET"])
        # list of default endpoints for all child Router class-objects                              -   ENDED   -
        
    def reinit(self):
        """=== Method name: reinit =====================================================================================
        to generate initial arguments depending on changed parameters
        ========================================================================================== by Sziller ==="""
        pass

    async def GET_basic_config(self):
        """=== Endpoint-method name: GET_basic_config ===  
        Endpoint returns minimal router data. This method is defined on parent level, thus all shmc routers provide
        some sort of actual state info under this path.  
        === by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        # request processing START                                                                  -   START   -
        data_dict = {"command": "GET_actual_state",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {},
                     "timestamp": timestamp}
        data = msg.InternalMsg.init_by_dict(**data_dict)
        # request processing ENDED                                                                  -   ENDED   -

        # action START                                                                              -   START   -
        payload = {'name': self.name, 'alias': self.alias, 'ip': self.ip, 'port': self.port, 'db_fullname': self.db_fullname, "db_style": self.db_style}
        # action ENDED                                                                              -   ENDED   -

        # responding START                                                                          -   START   -
        response = msg.ExternalResponseMsg(payload=payload,
                                           message="OK - sais {} on router: {}".format(cmn, self.ccn),
                                           timestamp=timestamp)
        return response
        # responding ENDED                                                                          -   ENDED   -
    
