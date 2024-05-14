"""
SQLAlchemy powered DB Bases: test, and production code.
by Sziller
"""

# imports for general Base handling START                                                   -   START   -
from sqlalchemy import Column, Integer, String, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
# imports for general Base handling ENDED                                                   -   ENDED   -

# imports for local Base handling   START                                                   -   START   -
from cryptography import HashFunctions as HaFu
# imports for local Base handling   ENDED                                                   -   ENDED   -

Base = declarative_base()


class User(Base):
    """=== Classname: User(Base) =======================================================================================
    Class represents general user who's data is to be stored and processed by the DB
    ============================================================================================== by Sziller ==="""
    __tablename__ = "users"
    uuid = Column("uuid", String, primary_key=True)
    email_list = Column("email_list", String)
    usr_fn = Column("usr_fn", String)
    usr_ln = Column("usr_ln", String)
    authorization = Column("authorization", Integer)
    pubkey = Column("pubkey", String)
    stripe_id = Column("stripe_id", String)
    timestamp = Column("timestamp", Float)

    def __init__(self,
                 uuid: str,
                 email_list: str,
                 usr_fn: str,
                 usr_ln: str = "",
                 authorization: int = 0,
                 pubkey: str or None = None,
                 stripe_id: str = "",
                 timestamp: float or None = None):
        self.uuid           = uuid
        self.email_list     = email_list
        self.usr_fn         = usr_fn
        self.usr_ln         = usr_ln
        self.authorization  = authorization
        self.pubkey         = pubkey
        self.stripe_id      = stripe_id
        self.timestamp      = timestamp

    def return_as_dict(self):
        """=== Method name: return_as_dict =============================================================================
        Returns instance as a dictionary
        @return : dict - parameter: argument pairs in a dict
        ========================================================================================== by Sziller ==="""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @ classmethod
    def construct(cls, d_in):
        """=== Classmethod: construct ==================================================================================
        Input necessary class parameters to instantiate object of the class!
        @param d_in: dict - format data to instantiate new object
        @return: an instance of the class
        ========================================================================================== by Sziller ==="""
        return cls(
            d_in["uuid"], d_in["email_list"], d_in["usr_fn"],
            d_in["usr_ln"], d_in["authorization"], d_in["pubkey"], d_in["stripe_id"])

    def __repr__(self):
        return "{:<33}:{:>4} {:<15} {:<15} - email: {:<35} - added: {}".format(self.uuid,
                                                                               self.authorization,
                                                                               self.usr_fn,
                                                                               self.usr_ln,
                                                                               self.email_list,
                                                                               self.timestamp)
