import time
import logging
import inspect
from shmc_routers._ShmcBaseRouter import ShmcBaseRouter
from shmc_sqlBases import SQL_basesRoom as sqlBroom
from shmc_sqlAccess import SQL_interface as sqli
from shmc_messages import msg
from shmc_messages import msg_room

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -


class RoomRouter(ShmcBaseRouter):
    """Class name: RoomRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name
    
    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str = "0.0.0.0",
                 port: int = 0,
                 db_fullname=None,
                 db_style=None):
        super().__init__(name, alias, ip, port, db_fullname, db_style)
        lg.debug("initiated : '{}' router as object {}".format(self.name, self.ccn))
        self.name: str                  = name
        self.alias: str                 = alias
        self.ip: str                    = ip
        self.port: int                  = port
        self.db_fullname: (str, None)   = db_fullname
        self.db_style: (str, None)      = db_style
        
        self.session                = None
    
        self.add_api_route("/v0/full-db-data",          self.GET_full_db_data,                      methods=["GET"])
    
    def reinit(self):
        """=== Method name: reinit =====================================================================================
        to generate initial arguments depending on changed parameters
        ========================================================================================== by Sziller ==="""
        self.session = sqli.createSession(db_fullname=self.db_fullname, tables=None, style="SQLite")
    
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------
    
    async def GET_full_db_data(self):
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
                                 'port': self.port,
                                 "session": self.session
                                 },
                     "timestamp": timestamp}
        data = msg_room.SrvrToRoomRequest.init_by_dict(**data_dict)
        # request processing ENDED                                                                  -   ENDED   -
        
        # action START                                                                              -   START   -
        payload = sqli.QUERY_entire_table(ordered_by="timestamp", row_obj=sqlBroom.Measurement, session=self.session)
        # action ENDED                                                                              -   ENDED   -

        # responding START                                                                          -   START   -
        response = msg.ExternalResponseMsg(payload=payload,
                                           message="OK - sais {} on router: {}".format(cmn, self.ccn),
                                           timestamp=timestamp)
        return response
        # responding ENDED                                                                          -   ENDED   -

    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
