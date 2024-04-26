""" Defining the basic message object to communicate inside SmartHome system
by Sziller"""


class MsgObject:
    """=== Class name: MsgObject ====================================================================================
    Two way communication Object between Server and Engine, Server and Subservers
    ============================================================================================== by Sziller ==="""
    def __init__(self, payload: dict, timestamp: float or None = None, **kwargs):
        # every communication message Object must have a timestamp defined on init:
        # this is the unique ID of the object on code level
        self.payload: dict              = payload
        self.timestamp: float or None   = timestamp

    def as_dict(self) -> dict:
        """=== Method name: as_dict ====================================================================================
        Returns actual state of instance as a dictionary.
        :return dict: parameter: args <- in current state
        ========================================================================================== by Sziller ==="""
        return {_: getattr(self, _) for _ in self.__dict__}

    @classmethod
    def init_by_dict(cls, **kwargs):
        """=== Classmethod name: generate_from_dict ====================================================================
        Lets you define an instance by dictionary
        ========================================================================================== by Sziller ==="""
        return cls(**kwargs)


class InternalMsg(MsgObject):
    def __init__(self, payload: dict, command: str, timestamp: float or None = None, **kwargs):
        super(InternalMsg, self).__init__(payload=payload, timestamp=timestamp, **kwargs)
        self.command: str       = command
        self.payload: dict      = payload
        self.timestamp: float   = timestamp


class ExternalResponseMsg(MsgObject):
    def __init__(self, payload: dict, message: str = "", timestamp: float or None = None, **kwargs):
        super(ExternalResponseMsg, self).__init__(payload=payload, timestamp=timestamp, **kwargs)
        self.message: str       = message
        self.payload: dict      = payload
        self.timestamp: float   = timestamp
        
