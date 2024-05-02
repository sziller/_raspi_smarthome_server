import time
import logging
import inspect
from shmc_routers._ShmcBaseRouter import ShmcBaseRouter

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -


class ObsrRouter(ShmcBaseRouter):
    """Class name: ObservatoryRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name
    
    def __init__(self, name: str, alias: str, ip: str = "0.0.0.0", port: int = 0, db_fullname=None, db_style=None):
        super().__init__(name, alias, ip, port, db_fullname, db_style)
        lg.debug("initiated : '{}' router as object {}".format(self.name, self.ccn))
        
    def reinit(self):
        """=== Method name: reinit =====================================================================================
        to generate initial arguments depending on changed parameters
        ========================================================================================== by Sziller ==="""
        pass
    
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------

    async def GET_actual_state(self):
        """=== Function name: GET_actual_state =============================================================================
        description...
        ============================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        # data_dict = {"command": "GET_actual_state",
        #              "user_id": "sziller_dev",
        #              "email": "szillerke@gmail.com",
        #              "signature": b'',
        #              "payload": {},
        #              "timestamp": timestamp}
        # data = msg_obsr.SrvrToAquaRequest.init_by_dict(**data_dict)
        # response = msg.ExternalResponseMsg(payload=data.payload,
        #                                    message="OK - sais {}".format(cmn),
        #                                    timestamp=timestamp)
        # return response.as_dict()
        return True
