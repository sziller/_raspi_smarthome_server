"""These are Router buliding blocks, responsible to create a Parent router for any usecase we use in SHMC development
Here is the hierarchical buildup.

# Hierarchy: (Attention! Endpoint authentication is not Router scope!)
# Ancestry:                 : example                   : added params              : added methods
# --------------------------:---------------------------:---------------------------:-----------------
# Engine connected          : Room, Observer            : zmq-port                  :
# Default Endpoints v. DB   : simple DB-handler         :                           : default EP-s
# DB handler                : AuthRouter                : db_fullname, db_style     :
# Authorized                :                           :                           : authorizer
# BaseRouter                :                           : name, alias, ip, port     :
# APIRouter                 : default FastApi class     :                           :


=== by Sziller ==="""

import os.path
import time
import logging
import inspect
from typing import Optional
from fastapi import APIRouter
from sz_messages import msg
from shmc_api_classes.auth_services import *
from sql_bases.sqlbase_measurement.sqlbase_measurement import Measurement as sqlMeasurement
from sql_access import sql_interface as sqli

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -


class BaseRouter(APIRouter):
    """=== Extended (APIRouter) class ==================================================================================
    Default Router parent class for Sziller's developments.
    ============================================================================================== by Sziller ==="""
    def __init__(self,
                 name: str,
                 alias: Optional[str],
                 ip: str = "0.0.0.0",
                 port: int = 0):
        super().__init__()
        self.name: str                          = name
        self.alias: str                         = alias if alias else name[:4]
        self.ip: str                            = ip  # ip of remote Engine and Message handler (zmq socket endpoint)
        self.port: int                          = port  # port remote server runs on - for DB communication
        lg.info(f"Initialized BaseRouter with"
                f"name='{self.name}', alias='{self.alias}', ip='{self.ip}', port='{self.port}'")

    def reinit(self):
        """=== Instance method =========================================================================================
        Reinitialization method for future use, depending on dynamic requirements.
        ========================================================================================== by Sziller ==="""
        lg.debug(f"{self.__class__.__name__} reinitialization called.")
    
    
class AuthorizedRouter(BaseRouter):
    """=== Extended class ==============================================================================================
    Extended Router class for for Sziller's developments.:
    - authorization logic added
    ============================================================================================== by Sziller ==="""
    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str = "0.0.0.0",
                 port: int = 0,
                 auth_dict: dict or None = None):
        super().__init__(name, alias, ip, port)
        self.auth_dict: dict = auth_dict
        lg.info(f"{self.__class__.__name__} initialized with auth_dict='{self.auth_dict}'")
        
    def check_authorization(self, auth_code: int, nth_switch: int):
        """=== Instance method =========================================================================================
        Function decides, whether an authorizatoin code includes certain binary digit.
        e.g.: 0-1-1-0 = 6   <- auth code
              3.2.1.0       <- pos.
        Function (6, 2) checks for position 2. and returns True
        Function (6, 0) checks for position 0. and returns False
        ========================================================================================== by Sziller ==="""
        lg.debug("authorize : using: {}".format(self.auth_dict))
        lg.debug("{} performing authorization check with auth_code={}, nth_switch={}"
                 .format(self.__class__.__name__, auth_code, nth_switch))
        result = auth_code & (1 << nth_switch) != 0
        lg.debug(f"Auth res. : {result}")
        return result
    

class DBHandlerRouter(AuthorizedRouter):
    """=== Extended class ==============================================================================================
    Extended Router class for for Sziller's developments.:
    -  handling database connections and data
    ============================================================================================== by Sziller ==="""
    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str = "0.0.0.0",
                 port: int = 0,
                 auth_dict: dict or None = None,
                 db_fullname: str or None = None,
                 db_style: str or None = None
                 ):
        super().__init__(name, alias, ip, port, auth_dict)
        self.db: list[dict] or None = None
        self.db_fullname: str       = db_fullname
        self.db_style: str          = db_style
    
    def reinit(self):
        """=== Method name: reinit =====================================================================================
        to generate initial arguments depending on changed parameters
        ========================================================================================== by Sziller ==="""
        super().reinit()
        lg.debug(f"{self.__class__.__name__} checking database file '{self.db_fullname}'")
        if self.db_fullname:
            if os.path.isfile(self.db_fullname):
                lg.info("found DB  : {} - says {}".format(self.db_fullname, self.__class__.__name__))
            else:
                lg.warning("no DB     : {} - says {}".format(self.db_fullname, self.__class__.__name__))
        else:
            lg.warning("undefined : database name - says {}".format(self.__class__.__name__))
    
    def read_db_table(self, row_obj: sqli.Base):
        """=== Method name: read_db ====================================================================================
        One time reading of the DB, defined by db_* parameters.
        Local session fot r this very method is created and closed right after reading out data into self.db
        ========================================================================================== by Sziller ==="""
        lg.debug(f"{self.__class__.__name__} attempting to read from DB '{self.db_fullname}'")
        try:
            loc_session = sqli.createSession(db_fullname=self.db_fullname, style=self.db_style, tables=None)
            self.db = sqli.QUERY_entire_table(ordered_by="timestamp", row_obj=row_obj, session=loc_session)
            loc_session.close()
            lg.info(f"read DB   : successfully from DB '{self.db_fullname}'")
        except Exception as e:
            lg.error(f"read DB   : Error reading DB '{self.db_fullname}': {e}")


class SkeletonRouter(DBHandlerRouter):
    """=== Class name: SkeletonRouter(DBHandlerRouter) =================================================================
    Router to include default Endpoints.
    Subclass of DBHandlerRouter.
    ============================================================================================== by Sziller ==="""    
    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str                    = "0.0.0.0",
                 port: int                  = 0,
                 auth_dict: dict or None    = None,
                 db_fullname: str or None   = None,
                 db_style: str or None      = None):
        super().__init__(name, alias, ip, port, auth_dict, db_fullname, db_style)
        # list of default endpoints for all child Router class-objects                              -   START   -
        self.add_api_route(path="/v0/basic-config",
                           endpoint=self.GET_basic_config,
                           response_model=msg.ExtRespMsg,
                           methods=["GET"])
        self.add_api_route(path="/v0/full-db-data",
                           endpoint=self.GET_full_db_data,
                           response_model=msg.ExtRespMsg,
                           methods=["GET"])
        # list of default endpoints for all child Router class-objects                              -   ENDED   -

    def reinit(self):
        """=== Instance method =========================================================================================
        Reinitialization method for future use, depending on dynamic requirements.
        ========================================================================================== by Sziller ==="""
        lg.debug(f"{self.__class__.__name__} reinitialization called.")
    
    async def GET_basic_config(self, 
                               current_user: UserInDB = Depends(AuthService.get_current_active_user)):
        """=== Endpoint-method name: GET_basic_config ===  
        Endpoint returns minimal router data. This method is defined on parent level, thus all shmc routers provide
        some sort of actual state info under this path.  
        === by Sziller ==="""
        timestamp = time.time()
        lg.info(f"GET_full_db_data called on router '{self.name}' at timestamp={timestamp}")
        # request processing START                                                                  -   START   -
        data_dict = {"command": "GET_actual_state",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {},
                     "timestamp": timestamp}
        data = msg.InternalMsg.init_by_dict(**data_dict)
        # request processing ENDED                                                                  -   ENDED   -

        # action START                                                                              -   START   -
        payload = {'name': self.name,
                   'alias': self.alias,
                   'ip': self.ip,
                   'port': self.port,
                   'db_fullname': self.db_fullname,
                   "db_style": self.db_style}
        # action ENDED                                                                              -   ENDED   -

        # responding START                                                                          -   START   -
        response = msg.ExtRespMsg(payload=payload,
                                  message="OK - says {} on router: {}".format(cmn, self.ccn),
                                  timestamp=timestamp)
        return response
        # responding ENDED                                                                          -   ENDED   -

    async def GET_full_db_data(self,
                               current_user: UserInDB = Depends(AuthService.get_current_active_user)):
        """=== Endpoint-method name: GET_full_db_data ===  
        Endpoint returns the usual response format, where 'payload' is the entire content of the DB  
        === by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        # request processing START                                                                  -   START   -
        timestamp = time.time()
        data_dict = {"command": "GET_full_db_data",
                     "user_id": "sziller_dev",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {'ip': self.ip,
                                 'port': self.port
                                 },
                     "timestamp": timestamp}
        data = msg.InternalMsg.init_by_dict(**data_dict)
        # request processing ENDED                                                                  -   ENDED   -

        # action START                                                                              -   START   -
        session = sqli.createSession(db_fullname=self.db_fullname, tables=None, style=self.db_style)
        payload = sqli.QUERY_entire_table(ordered_by="timestamp", row_obj=sqlMeasurement, session=session)
        # action ENDED                                                                              -   ENDED   -

        # responding START                                                                          -   START   -
        response = msg.ExtRespMsg(payload=payload,
                                  message="OK - says {} on router: {}".format(cmn, self.ccn),
                                  timestamp=timestamp)
        return response
        # responding ENDED                                                                          -   ENDED   -


class EngineMngrRouter(SkeletonRouter):
    """=== Extended class ==============================================================================================
    Extended Router class for for Sziller's developments.:
    -  handling background Engines
    ============================================================================================== by Sziller ==="""
    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str                    = "0.0.0.0",
                 port: int                  = 0,
                 auth_dict: Optional[dict]  = None,
                 db_fullname: Optional[str] = None,
                 db_style: Optional[str]    = None,
                 zmq_port: int              = 0):       # port of remote Message handler (zmq socket endpoint)
        super().__init__(name, alias, ip, port, auth_dict, db_fullname, db_style)
        self.zmq_port: int          = zmq_port
        lg.info(f"{self.__class__.__name__} initialized with zmq_port='{self.zmq_port}'")

    def reinit(self):
        """=== Method name: reinit =====================================================================================
        Possible script meant to be run right after instantiation.
        ========================================================================================== by Sziller ==="""
        super().reinit()
        lg.debug(f"{self.__class__.__name__} reinitialization: zmq_port={self.zmq_port}")
