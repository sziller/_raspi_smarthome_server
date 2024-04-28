import time
import logging
import inspect
from fastapi import APIRouter
from shmc_messages import msg
from shmc_messages import msg_obsr

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -


class ObsrRouter(APIRouter):
    """Class name: ObservatoryRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name
    
    def __init__(self, nr: int = 0):
        super().__init__()
        lg.debug("initiated : {} - as object".format(self.ccn))
        self.nr_of_fish = nr
        
        self.add_api_route("/v0/actual-state", self.GET_actual_state, methods=["GET"])
    
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
