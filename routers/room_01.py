from fastapi import APIRouter
import time
import inspect
from sh_msg import msg
from sh_msg import msg_obsr

room01_router = APIRouter()


@room01_router.get("/v0/actual-state")                                                            # GET: v0/actual-state
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
    data = msg_obsr.SrvrToObsrRequest.init_by_dict(**data_dict)
    response = msg.ExternalResponseMsg(payload=data.payload,
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()
