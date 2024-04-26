import time

from fastapi import APIRouter
import inspect
import config as conf
from sh_msg import msg
from sh_msg import msg_room

from RoomManager import DataBaseAlchemy as DBAl

if conf.isDIRECT_SETUP:  # Direct outside connection: No Server in the network in front of this API towards Internet
    pass
else:  # Indirect outside connection: There IS a Server in the network - forwarding requests, processing answers
    pass

room_01_router = APIRouter()
process_engine = None

# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   START   -
# -------------------------------------------------------------------------------------------------------------------


@room_01_router.get("/v0/actual-state")                                                            # GET: v0/actual-state
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
    data = msg_room.SrvrToAquaRequest.init_by_dict(**data_dict)
    
    session = DBAl.createSession(conf.DATABASE_NAME)
    actual_values = DBAl.QUERY_rows_by_column_filtervalue_list_ordered(filterkey="msmnt_loc",
                                                                       filtervalue_list=["room_01"],
                                                                       ordered_by="timestamp",
                                                                       db_table="measurements",
                                                                       session_in = session
                                                                       )
    
    response = msg.ExternalResponseMsg(payload=actual_values[-3:],
                                       message="OK - sais {}".format(cmn),
                                       timestamp=timestamp)
    return response.as_dict()


# -------------------------------------------------------------------------------------------------------------------
# - Endpoints                                                                               Endpoints   -   ENDED   -
# -------------------------------------------------------------------------------------------------------------------
