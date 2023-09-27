"""Messages sent to and from the Aquaponic system
by Sziller"""

from time_format import TimeFormat as TiFo
from .msg import *  # importing base msg object to create subclasses from

class OBRequest(MsgObject):
    """
    
    """
    def __init__(self, command: str, user_id: str, email: str, signature: bytes, payload: dict, timestamp: float):
        super(OBRequest, self).__init__(timestamp)
        self.command: str               = command
        self.user_id: str               = user_id
        self.email: str                 = email
        self.signature: bytes or None   = signature
        self.payload: dict              = payload
        self.timestamp: str             = TiFo.format_timestamp_raw(timestamp_raw=timestamp)

    @classmethod
    def generate_from_dict(cls, dict_in):
        """=== Classmethod name: generate_from_dict ====================================================================
        Lets you define an instance by dictionary
        ========================================================================================== by Sziller ==="""
        return cls(dict_in["command"],
                   dict_in["user_id"],
                   dict_in["email"],
                   dict_in["signature"],
                   dict_in["payload"],
                   dict_in["timestamp"])


