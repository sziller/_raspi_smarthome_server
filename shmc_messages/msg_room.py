"""Messages sent to and from the Aquaponic system
by Sziller"""

from time_format import TimeFormat as TiFo
from .msg import *  # importing base msg object to create subclasses from


class SrvrToRoomRequest(InternalMsg):
    """=== Message name: SrvrToAquaRequest =============================================================================
    ============================================================================================== by Sziller ==="""
    def __init__(self, command: str, email: str, signature: bytes, payload: dict, timestamp: float, **kwargs):
        super(SrvrToRoomRequest, self).__init__(payload=payload, command=command, timestamp=timestamp, **kwargs)
        self.command: str               = command
        self.email: str                 = email
        self.signature: bytes or None   = signature
        self.payload: dict              = payload
        self.timestamp: str             = TiFo.format_timestamp_raw(timestamp_raw=timestamp)
