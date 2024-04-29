import time
import logging
import inspect
from fastapi import APIRouter
from shmc_messages import msg
from shmc_messages import msg_room

# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -


class RoomRouter(APIRouter):
    """Class name: RoomRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name
    
    def __init__(self, name: str = ""):
        super().__init__()
        lg.debug("initiated : {} - as object".format(self.ccn))
        self.name = name
    
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
        data_dict = {"command": "GET_actual_state",
                     "user_id": "sziller_dev",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {},
                     "timestamp": timestamp}
        # data = msg_room.SrvrToAquaRequest.init_by_dict(**data_dict)
        # 
        # session = DBAl.createSession(conf.DATABASE_NAME)
        # actual_values = DBAl.QUERY_rows_by_column_filtervalue_list_ordered(filterkey="msmnt_loc",
        #                                                                    filtervalue_list=["room_01"],
        #                                                                    ordered_by="timestamp",
        #                                                                    db_table="measurements",
        #                                                                    session_in = session
        #                                                                    )
        # 
        # response = msg.ExternalResponseMsg(payload=actual_values[-3:],
        #                                    message="OK - sais {}".format(cmn),
        #                                    timestamp=timestamp)
        return True

    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
