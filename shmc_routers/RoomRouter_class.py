from fastapi import APIRouter


class RoomRouter(APIRouter):
    """Class name: RoomRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    def __init__(self, nr: int = 0):
        super().__init__()
        print("instantiated: {}".format(self))
        self.nr_of_fish = nr
