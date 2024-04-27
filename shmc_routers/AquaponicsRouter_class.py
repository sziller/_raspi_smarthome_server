from fastapi import APIRouter


class AquaponicsRouter(APIRouter):
    """Class name: AquaponicsRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    def __init__(self, nr: int = 0):
        super().__init__()
        print("instantiated: {}".format(self))
        self.nr_of_fish = nr
