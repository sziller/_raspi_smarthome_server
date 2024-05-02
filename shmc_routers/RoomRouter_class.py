import time
import logging
import inspect
from shmc_routers._ShmcBaseRouter import ShmcBaseRouter

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

    # list of default endpoints for all child Router class-objects                              -   START   -

    # list of default endpoints for all child Router class-objects                              -   ENDED   -
    
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
