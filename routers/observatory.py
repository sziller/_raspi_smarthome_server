from fastapi import APIRouter
import time
import inspect
from sh_msg import msg_obsr

observatory_router = APIRouter()


@observatory_router.get("/v0/actual-state")                                                            # GET: v0/actual-state
async def GET_actual_state():
    """=== Function name: GET_actual_state =============================================================================
    description...
    ============================================================================================== by Sziller ==="""
    timestamp = time.time()
    data_dict = {"command": "GET_actual_state",
                 "user_id": "sziller_dev",
                 "email": "szillerke@gmail.com",
                 "signature": b'',
                 "payload": {},
                 "timestamp": timestamp}
    data = msg_obsr.SrvrToObsrRequest.init_by_dict(dict_in=data_dict)
    return data.as_dict()
