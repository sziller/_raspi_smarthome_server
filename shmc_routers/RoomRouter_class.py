import logging
import inspect
from shmc_routers._ShmcBaseRouters import EngineMngrRouter

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -


class RoomRouter(EngineMngrRouter):
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

    # list of default endpoints for all child Router class-objects                              -   ENDED   -
    
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
