from fastapi import APIRouter


class ObservatoryRouter(APIRouter):
    """Class name: ObservatoryRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    def __init__(self, nr: int = 0):
        super().__init__()
        print("instantiated: {}".format(self))
        self.nr_of_fish = nr
