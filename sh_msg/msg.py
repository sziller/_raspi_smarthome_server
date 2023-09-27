""" Defining the basic message object to communicate inside SmartHome system
by Sziller"""


class MsgObject:
    """=== Class name: MsgObject ====================================================================================
    Two way communication Object between Server and Engine, Server and Subservers
    ============================================================================================== by Sziller ==="""
    def __init__(self, payload: dict, timestamp: float or None = None):
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
    def init_by_dict(cls, dict_in):
        """=== Classmethod name: generate_from_dict ====================================================================
        Lets you define an instance by dictionary
        ========================================================================================== by Sziller ==="""
        return cls(**dict_in)


class InternalMsg(MsgObject):
    def __init__(self, command: str, payload: dict, timestamp: float or None = None):
        super(InternalMsg, self).__init__(payload, timestamp)
        self.command: str       = command


class ExternalResponseMsg(MsgObject):
    def __init__(self, payload: dict, message: str = "", timestamp: float or None = None):
        super(ExternalResponseMsg, self).__init__(payload, timestamp)
        self.message: str       = message
