import time

from fastapi import APIRouter
import inspect
import config as conf
from shmc_messages import msg
from shmc_messages import msg_obsr

if conf.isDIRECT_SETUP:  # Direct outside connection: No Server in the network in front of this API towards Internet
    pass
else:  # Indirect outside connection: There IS a Server in the network - forwarding requests, processing answers
    pass

observatory_router = APIRouter()
process_engine = None

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   START   -
# -------------------------------------------------------------------------------------------------------------------


@observatory_router.get("/v0/actual-state")                                                            # GET: v0/actual-state
async def GET_actual_state():
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
    data = msg_obsr.SrvrToAquaRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()


# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------
