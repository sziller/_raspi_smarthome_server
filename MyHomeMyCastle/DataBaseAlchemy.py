"""
[cols ="1n, 1n, 1n, 5, f, a, a, a", frame=none, grid=none, options="header"]
.Table 1. - <records>
|=======================================================================================================================
|=======================================================================================================================
"""
import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Column, Float, Integer, String, JSON
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import close_all_sessions
import config as conf
from cryptography import HashFunctions as HaFu
from time_format import TimeFormat as TiFo

Base = declarative_base()


def createSession(db_path: str, style: str = "SQLite", base=Base):
    """=== Function name: createSession ================================================================================
    ============================================================================================== by Sziller ==="""
    if style == "SQLite":
        engine = create_engine('sqlite:///%s' % db_path, echo=False, poolclass=NullPool)
    elif style == "PostGreSQL":
        engine = create_engine(db_path, echo=False, poolclass=NullPool)
    else:
        raise Exception("no valid dialect defined")

    base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

# CLASS definitions ENDED                                                                   -   START   -


class ScheduledTask(Base):
    """=== Classname: ScheduledTask(Base) ============================================================================
    Class represents scheduled task who's data is to be stored and processed by the DB
    ============================================================================================== by Sziller ==="""
    __tablename__ = "scheduledtasks"
    id_hash     = Column("id_hash", String, primary_key=True)
    style       = Column("style", Integer)
    task_name   = Column("task_name", String)
    init_at     = Column("init_at", Integer)
    step_size   = Column("step_size", Integer)

    def __init__(self,
                 task_name: str,
                 init_at: int,
                 step_size: int,
                 style: int,
                 id_hash: str   = "",
                 ):
        self.task_name  = task_name
        self.init_at    = init_at
        self.step_size  = step_size
        self.style      = style
        self.id_hash    = id_hash
        
        self.generate_id_hash()
    
    def generate_id_hash(self):
        """Function adds a unique ID to the row"""
        self.id_hash = HaFu.single_sha256_byte2byte(bytes(
            "{}{}".format(self.task_name, self.style),
            "utf-8")).hex()
    
    def return_as_dict(self):
        """=== Method name: return_as_dict =============================================================================
        Returns instance as a dictionary
        @return : dict - parameter: argument pairs in a dict
        ========================================================================================== by Sziller ==="""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def construct(cls, d_in):
        """=== Classmethod: construct ==================================================================================
        Input necessary class parameters to instantiate object of the class!
        @param d_in: dict - format data to instantiate new object
        @return: an instance of the class
        ========================================================================================== by Sziller ==="""
        return cls(
            d_in["task_name"], d_in["init_at"], d_in["step_size"], d_in["style"])
    
    
class RestrictedIP(Base):
    """=== Classname: RestrictedIP(Base) ===============================================================================
    Class represents IP restrictions who's data is to be stored and processed by the DB
    ============================================================================================== by Sziller ==="""
    __tablename__ = "restrictedips"
    ip      = Column("ip", String, primary_key=True)
    date    = Column("date", String)
    used    = Column("used", Integer)

    def __init__(self, ip: str, date: str, used: int):
        self.ip: str        = ip
        self.date: str      = date
        self.used: int      = used
    
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
        return cls(d_in["ip"], d_in["date"], d_in["used"])


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
    timestamp = Column("timestamp", Float)

    def __init__(self,
                 uuid: str,
                 email_list: str,
                 usr_fn: str,
                 usr_ln: str = "",
                 authorization: int = 0,
                 pubkey: str or None = None,
                 timestamp: float or None = None,
                 ):
        self.uuid           = uuid
        self.email_list     = email_list
        self.usr_fn         = usr_fn
        self.usr_ln         = usr_ln
        self.authorization  = authorization
        self.pubkey         = pubkey
        self.timestamp      = TiFo.timestamp(formatted=False)

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
            d_in["usr_ln"], d_in["authorization"], d_in["pubkey"])

    def __repr__(self):
        return "{:<33}:{:>4} {:<15} {:<15} - email: {:<35} - added: {}".format(self.uuid,
                                                                               self.authorization,
                                                                               self.usr_fn,
                                                                               self.usr_ln,
                                                                               self.email_list,
                                                                               self.timestamp)


class Document(Base):
    """=== Classname: Document(Base) ===================================================================================
    Class represents general document who's data is to be stored and processed by the DB
    ============================================================================================== by Sziller ==="""
    __tablename__ = "documents"
    hash_hxstr      = Column("hash_hxstr", String, primary_key=True)
    uuid            = Column("uuid", String)
    location_list   = Column("location_list", JSON)
    docdata_dict    = Column("docdata_dict", JSON)
    timestamp       = Column("timestamp", Float)

    def __init__(self,
                 hash_hxstr: str,
                 uuid: str,
                 location_list: list,
                 docdata_dict: dict = {},
                 timestamp: float or None = None,
                 ):
        self.hash_hxstr         = hash_hxstr
        self.uuid               = uuid
        self.location_list      = location_list
        # check = {
        #     "1": "250810a82a2ceba579620b5aa969556e97f0cda454234abce4372a937017a2dd",
        #     "0000": "17194c09e3ce98e582a064d4e46edd184f077b48f22dff81ae75bbf43cb4cd5a",
        #     "001": "82be000d47e93883c89e565abbb8f67167556e95bef6eb64663696cc386d1a09",
        #     "01": "fbee6179a3bae7e2810a3491de870522ae3f0342b22bda7f81d0b07b3f3320f1"
        #     }
        # check = ["szillerke@gmail.com", "johnny@freemail.hu"]
        self.docdata_dict       = docdata_dict
        self.timestamp          = TiFo.timestamp(formatted=False)

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
            d_in["hash_hxstr"], d_in["uuid"], d_in["location_list"], d_in["docdata_dict"])

    def __repr__(self):
        return "{:<33}:{:<33}{:<40}\n{}".format(self.hash_hxstr,
                                                self.uuid,
                                                self.location_list,
                                                self.docdata_dict)


class Record(Base):
    """=== Classname: Record(Base) =====================================================================================
    Class represents general record who's data is to be stored and processed by the DB
    ============================================================================================== by Sziller ==="""
    __tablename__   = "records"
    hash_hxstr      = Column("hash_hxstr",      String, primary_key=True)
    # hash_bytes      = Column("hash_bytes",      LargeBinary)
    email           = Column("email",           String)
    email_sent      = Column("email_sent",      Float)
    mrkl_root_list  = Column("mrkl_root_list",  String)
    mrkl_addr_list  = Column("mrkl_addr_list",  String)
    rights          = Column("rights",          Integer)
    timestamp       = Column("timestamp",       Float)

    def __init__(self,
                 hash_hxstr: str,
                 email: str,
                 email_sent: float = 0.0,
                 mrkl_root_list: str = "",
                 mrkl_addr_list: str = "",
                 rights: int = 0
                 ):

        self.hash_hxstr: str                = hash_hxstr
        # self.hash_bytes: bytes              = bytes.fromhex(self.hash_hxstr)
        self.email: str                     = email
        self.email_sent: float                = email_sent
        self.mrkl_root_list: str   = mrkl_root_list
        self.mrkl_addr_list:  str  = mrkl_addr_list
        self.rights: int                    = rights
        self.timestamp = TiFo.timestamp(formatted=False)

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
        return cls(d_in["hash_hxstr"], d_in["email"])

    def __repr__(self):
        return "{:<33}:{:>35} - added: {}".format(self.hash_hxstr,
                                                  self.email,
                                                  self.timestamp)


class MerkleTree(Base):
    """=== Classname: MerkleTree(Base) =================================================================================
    Class represents general merkle tree who's data is to be stored and processed by the DB
    ============================================================================================== by Sziller ==="""
    __tablename__ = "merkletrees"
    root_hxstr      = Column("root_hxstr", String, primary_key=True)
    proofdata       = Column("proofdata", JSON)
    timestamp       = Column("timestamp", Float)
    txhash          = Column("txhash", String)
    txraw           = Column("txraw", String)
    txpublished     = Column("txpublished", Float)
    txconfirmed     = Column("txconfirmed", Float)
    snr             = Column("snr", Integer)

    def __init__(self,
                 root_hxstr: str,
                 proofdata: dict,
                 txhash: str,
                 txraw: str             = "",
                 txpublished: float     = 0.0,
                 txconfirmed: float     = 0.0,
                 snr: int               = snr,
                 timestamp: float       = 0.0,
                 ):
        self.root_hxstr: str            = root_hxstr
        self.proofdata: dict            = proofdata
        self.txhash: str                = txhash
        self.txraw: str                 = txraw
        self.txpublished: float         = txpublished
        self.txconfirmed: float         = txconfirmed
        self.snr: int                   = snr
        self.timestamp: float  = TiFo.timestamp(formatted=False)

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
        return cls(d_in["root_hxstr"],
                   d_in["proofdata"],
                   d_in["txhash"],
                   d_in["txraw"],
                   d_in["txpublished"],
                   d_in["txconfirmed"],
                   d_in["snr"])

    def __repr__(self):
        return "{:<33}:{}".format(self.root_hxstr, self.proofdata)


# CLASS definitions ENDED                                                                   -   ENDED   -
# CLASS assignment to tables START                                                          -   START   -
OBJ_KEY = {conf.DB_ID_TABLE_USERS: User,
           conf.DB_ID_TABLE_DOCUMENTS: Document,
           conf.DB_ID_TABLE_SCHEDULED: ScheduledTask,
           conf.DB_ID_TABLE_IPS: RestrictedIP}
# CLASS assignment to tables ENDED                                                          -   ENDED   -


def ADD_rows_to_table(primary_key: str,
                      data_list: list,
                      db_table: str,
                      db_path: str = "",
                      style: str = "",
                      session_in: object or None = None):
    """
    @param primary_key: 
    @param data_list: 
    @param db_path: 
    @param db_table: 
    @param style: 
    @param session_in: 
    @return: 
    """
    if session_in:
        session = session_in
    else:
        session = createSession(db_path=db_path, style=style)
    global OBJ_KEY
    RowObj = OBJ_KEY[db_table]
    for data in data_list:
        if primary_key in data:  # works only if primary key is set and included in row to be created!
            if not session.query(RowObj).filter(getattr(RowObj, primary_key) == data[primary_key]).count():
                newrow = RowObj.construct(d_in=data)
                session.add(newrow)
        else:
            # this is the general case. <data> doesn't need to include primary key:
            # we check if primary key having been generated on instantiation exists.
            newrow = RowObj.construct(d_in=data)
            if not session.query(RowObj).filter(getattr(RowObj, primary_key) == getattr(newrow, primary_key)).count():
                session.add(newrow)
    session.commit()
    if not session_in:
        session.close()


def db_delete_table(db_path, dellist: list, style: str):
    """

    @return:
    """
    cmn = inspect.currentframe().f_code.co_name  # current method name
    if style == "SQLite":
        engine = create_engine('sqlite:///%s' % db_path, echo=True)
    elif style == "PostGreSQL":
        engine = create_engine(db_path, echo=True)
    else:
        raise Exception("<style> not recognized. - sais {}".format(cmn))
    
    Base.metadata.create_all(bind=engine)
    if "users" in dellist:
        User.__table__.drop(engine)
    if "documents" in dellist:
        Document.__table__.drop(engine)
    if "merkletrees" in dellist:
        MerkleTree.__table__.drop(engine)
    if "records" in dellist:
        Record.__table__.drop(engine)
    if "scheduledtasks" in dellist:
        ScheduledTask.__table__.drop(engine)


def drop_table(table_name, engine):
    """
    @param table_name: 
    @param engine: 
    @return: 
    """
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    if table is not None:
        Base.metadata.drop_all(engine, [table], checkfirst=True)


def db_delete_multiple_usrs_by_key(key: str, filtervalue_list: list, db_path: str, style: str):
    """=== Function name: db_delete_multiple_usrs_by_key ==============================================================
    @param key: str - name of row's attribute
    @param filtervalue_list: list - list of values's of rows to be deleted
    @return:
    ============================================================================================== by Sziller ==="""
    session = createSession(db_path=db_path, style=style)
    for filtervalue in filtervalue_list:
        session.query(User).filter(getattr(User, key) == filtervalue).delete(synchronize_session=False)
    session.commit()
    # if not session_in:
    session.close()


def db_delete_multiple_docs_by_key(key: str, filtervalue_list: list, db_path: str, style: str):
    """=== Function name: db_delete_multiple_docs_by_key ==============================================================
    @param key: str - name of row's attribute
    @param filtervalue_list: list - list of values of rows to be deleted
    @param db_path: str - the actual DataBase name the engine uses. Different for SQLite and PostGreSQL
    @param style: str - to distinguish path handling, enter DB style : PostGreSQL or SQLite
    @return:
    ============================================================================================== by Sziller ==="""
    session = createSession(db_path=db_path, style=style)
    for filtervalue in filtervalue_list:
        session.query(Document).filter(getattr(Document, key) == filtervalue).delete(synchronize_session=False)
    session.commit()
    session.close()
    # if not session_in:
    session.close()


def MODIFY_multiple_rows_by_column_to_value(
        filterkey: str,
        filtervalue_list: list,
        target_key: str,
        target_value,
        db_table: str,
        db_path: str    = "",
        style: str      = "",
        session_in: object or None = None):
    """=== Function name: db_REC_modify_multiple_rows_by_column_to_value ===============================================
    USE THIS IF THE NEW VALUES THE CELLS MUST TAKE ARE IDENTICAL!!!
    This function deals with the USERs DB Table!!!
    @param filterkey: str - name of column, in which filtervalues will be looked for
    @param filtervalue_list: list - list of values of rows to be deleted
    @param target_key: str - name of the column, whose value will be modified
    @param target_value: any data to be put into multiple cell
    @param db_path: str - the actual DataBase name the engine uses. Different for SQLite and PostGreSQL
    @param db_table: str - name of the table you want to write
    @param style: str - to distinguish path handling, enter DB style : PostGreSQL or SQLite
    @param session_in: obj - a precreated session. If used, it will not be closed. If not entered, a new session is
                                                    created, which is closed at the end.
    @return:
    ============================================================================================== by Sziller ==="""
    if session_in:
        session = session_in
    else:
        session = createSession(db_path=db_path, style=style)
    global OBJ_KEY
    RowObj = OBJ_KEY[db_table]
    for filtervalue in filtervalue_list:
        session.query(RowObj).filter(getattr(RowObj, filterkey) == filtervalue).update({target_key: target_value})
    session.commit()
    if not session_in:
        session.close()


def MODIFY_multiple_rows_by_column_by_dict(filterkey: str,
                                           mod_dict: dict,
                                           db_table,
                                           db_path: str = "",
                                           style: str = "",
                                           session_in: object or None = None):
    """
    
    @param filterkey: 
    @param mod_dict: 
    @param db_path: 
    @param db_table: 
    @param style: 
    @param session_in:
    @return: 
    """
    if session_in:
        session = session_in
    else:
        session = createSession(db_path=db_path, style=style)
    global OBJ_KEY
    RowObj = OBJ_KEY[db_table]
    for filtervalue, sub_dict in mod_dict.items():
        session.query(RowObj).filter(getattr(RowObj, filterkey) == filtervalue).update(sub_dict)
    session.commit()
    if not session_in:
        session.close()


def QUERY_entire_table(ordered_by: str,
                       db_table: str,
                       db_path: str = "",
                       style: str = "",
                       session_in: object or None = None) -> list:
    """=== Function name: QUERY_entire_table =========================================================================
    Function returns an entire DB table, defined by args.
    This function deals with the entered DB Table!!!
    @param ordered_by:
    @param db_path:
    @param db_table:
    @param style:
    @param session_in:
    @return: list of rows in table requested.
    ========================================================================================== by Sziller ==="""
    if session_in:
        session = session_in
    else:
        session = createSession(db_path=db_path, style=style)
    global OBJ_KEY
    RowObj = OBJ_KEY[db_table]
    results = session.query(RowObj).order_by(ordered_by).all()
    result_list = [_.return_as_dict() for _ in results]
    session.commit()
    if not session_in:
        session.close()
    return result_list


def QUERY_rows_by_column_filtervalue_list_ordered(filterkey: str,
                                                  filtervalue_list: list,
                                                  ordered_by: str,
                                                  db_table: str,
                                                  db_path: str = "",
                                                  style: str = "",
                                                  session_in: object or None = None) -> list:

    """=== Function name: QUERY_rows_by_column_filtervalue_list_ordered =============================================
    This function deals with the entered DB Table!!!
    @param filterkey:
    @param filtervalue_list:
    @param ordered_by:
    @param db_path:
    @param db_table:
    @param style:
    @param session_in:
    @return:
    ============================================================================================== by Sziller ==="""
    if session_in:
        session = session_in
    else:
        session = createSession(db_path=db_path, style=style)
    global OBJ_KEY
    RowObj = OBJ_KEY[db_table]
    '''
    rec_results = []
    for filtervalue in filtervalue_list:
        rec_subresults = session.query(RowObj).filter(getattr(RowObj, filterkey) == filtervalue).order_by(ordered_by).all()
        rec_results += rec_subresults
        '''
    # rec_results = session.query(RowObj).filter(getattr(RowObj, filterkey) in filtervalue_list).order_by(ordered_by).all()
    # rec_results = session.query(RowObj).filter(RowObj.hash_hxstr.in_(tuple(filtervalue_list)))

    results = session.query(RowObj).filter(getattr(RowObj, filterkey).in_(tuple(filtervalue_list))).order_by(ordered_by)
    result_list = [_.return_as_dict() for _ in results]
    session.commit()
    if not session_in:
        session.close()
    return result_list


if __name__ == "__main__":
    import time
    _filterkey = "hash_hxstr"
    _filtervalue_list = \
        ['7183e898ce742e221d900024665f8e67030e751f3dc35161de53cc4caca2729a',
         '7bd7421c17294f3b7e7572fdeb50b23b7480f17604786af11f5b96873c6ff7b3',
         'b3bb8e49abf70fe1e92063016fe857e4a6eb9d5316828bf49d22165c29d2a8e8',
         '7bd7421c17294f3b7e7572fdeb50b23b7480f17604786af11f5b96873c6ff7b3',
         '0000111100001111000011110000111100001111000011110000111100001111',
         '4bf52ecbd77c1b28bffb89d4e97278d6a236c837c7cab1ed3ea032bcaa34518d',
         '0000111100001111000011110000111100001111000011110000111100002222']
    _ordered_by = "hash_hxstr"
    
    import config_live
    _db_path = config_live.DATABASE_NAME
    _style = config_live.DATABASE_STYLE
    
    import config_dev
    _db_path = config_dev.DATABASE_NAME
    _style = config_dev.DATABASE_STYLE
    
    print(_db_path)
    _db_table = "documents"
    
    n_times = 5000
    
    default_session = createSession(db_path=_db_path, style=_style)
    start = time.time()
    for count in range(n_times):
        li = QUERY_rows_by_column_filtervalue_list_ordered(filterkey=_filterkey,
                                                           filtervalue_list=_filtervalue_list,
                                                           ordered_by=_ordered_by,
                                                           db_table=_db_table,
                                                           session_in=default_session)
        # print(li)
        assigned = {_['hash_hxstr']: _['location_list'] for _ in li}
        email_filelist = [assigned.get(_)[0].split(sep="/")[-1] if _ in assigned else '< not available >' for _ in _filtervalue_list]
        # for _ in email_filelist:
        #     print(_)
    print(int(time.time() - start))

    start = time.time()
    for count in range(n_times):
        li = QUERY_rows_by_column_filtervalue_list_ordered(filterkey=_filterkey,
                                                           filtervalue_list=_filtervalue_list,
                                                           ordered_by=_ordered_by,
                                                           db_table=_db_table,
                                                           db_path=_db_path,
                                                           style=_style,
                                                           session_in=None)
        # print(li)
        assigned = {_['hash_hxstr']: _['location_list'] for _ in li}
        email_filelist = [assigned.get(_)[0].split(sep="/")[-1] if _ in assigned else '< not available >' for _ in
                          _filtervalue_list]
        # for _ in email_filelist:
        #     print(_)
    print(int(time.time() - start))
