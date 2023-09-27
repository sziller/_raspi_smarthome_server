"""Messages sent to and from the Aquaponic system
by Sziller"""

from time_format import TimeFormat as TiFo
from .msg import *  # importing base msg object to create subclasses from


class SrvrToAquaRequest(InternalMsg):
    """=== Message name: SrvrToAquaRequest =============================================================================
    ============================================================================================== by Sziller ==="""
    def __init__(self, command: str, email: str, signature: bytes, payload: dict, timestamp: float, **kwargs):
        super(SrvrToAquaRequest, self).__init__(payload=payload, command=command, timestamp=timestamp, **kwargs)
        self.command: str               = command
        self.email: str                 = email
        self.signature: bytes or None   = signature
        self.payload: dict              = payload
        self.timestamp: str             = TiFo.format_timestamp_raw(timestamp_raw=timestamp)
        
        
class SrvrToUserResponse(ExternalResponseMsg):
    """=== Message name: SrvrToUserResponse ============================================================================
    ============================================================================================== by Sziller ==="""

    def __init__(self, message: str, payload: dict, timestamp: float, **kwargs):
        super(SrvrToUserResponse, self).__init__(payload=payload, message=message, timestamp=timestamp, **kwargs)
        self.message: str = message
        self.payload: dict = payload
        self.timestamp: str = TiFo.format_timestamp_raw(timestamp_raw=timestamp)
    
