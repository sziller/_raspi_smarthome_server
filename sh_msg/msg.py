""" Defining the basic message object to communicate inside SmartHome system
by Sziller"""


class MsgObject:
    """=== Class name: MsgObject ====================================================================================
    Two way communication Object between Server and Engine, Server and Subservers
    ============================================================================================== by Sziller ==="""
    def __init__(self, timestamp: float or None = None):
        # every communication message Object must have a timestamp defined on init:
        # this is the unique ID of the object on code level
        self.timestamp: float or None = timestamp

    def as_dict(self) -> dict:
        """=== Method name: as_dict ====================================================================================
        Returns actual state of instance as a dictionary.
        :return dict: parameter: args <- in current state
        ========================================================================================== by Sziller ==="""
        return {_: getattr(self, _) for _ in self.__dict__}
    
