import os
import time
from fastapi import Depends
from datetime import datetime, timedelta
import logging
import inspect
from shmc_routers._ShmcBaseRouter import ShmcBaseRouter
from shmc_routers.auth import *
from shmc_messages import msg
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Depends, HTTPException, status
from jose import jwt


# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
AUTH_ALGO = os.getenv("AUTH_ALGO")
AUTH_TOKEN_EXPIRE_MINS = os.getenv("AUTH_TOKEN_EXPIRE_MINS")


def create_access_token(data: dict, expires_delta: (timedelta, None) = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGO)
    return encoded_jwt


class AuthRouter(ShmcBaseRouter):
    """Class name: RoomRouter ====================================================================================
    ============================================================================================== by Sziller ==="""
    ccn = inspect.currentframe().f_code.co_name  # current class name

    def __init__(self,
                 name: str,
                 alias: str,
                 ip: str = "0.0.0.0",
                 port: int = 0,
                 zmq_port: int = 0,
                 db_fullname=None,
                 db_style=None):
        super().__init__(name, alias, ip, port, db_fullname, db_style)
        lg.debug("initiated : '{}' router as object {}".format(self.name, self.ccn))
        self.name: str = name
        self.alias: str = alias
        self.ip: str = ip  # ip of remote Engine and Message handler (zmq socket endpoint)
        self.port: int = port  # port remote server runs on - for DB communication
        self.zmq_port: int = zmq_port  # port of remote Message handler (zmq socket endpoint)
        self.db_fullname: (str, None) = db_fullname
        self.db_style: (str, None) = db_style
        
        self.db_fullname_shmc = os.getenv("DB_FULLNAME_SHMC")
        self.db_style = os.getenv("DB_STYLE")
        
        self.session = SQLi.createSession(db_fullname=self.db_fullname_shmc,
                                          style=self.db_style,
                                          tables=None)
        self.db = SQLi.QUERY_entire_table(ordered_by="timestamp", row_obj=sqlUser, session=self.session)
        
        print("+++++++++++++++++++")
        print(os.getenv("DB_FULLNAME_SHMC"))
        print(os.getenv("DB_STYLE"))
        print(self.session)
        for _ in self.db:
            print(_)
        print("+++++++++++++++++++")
        
        # list of default endpoints for all child Router class-objects                              -   START   -
        self.add_api_route(path="/token", endpoint=self.POST_login_for_access_token, response_model=Token, methods=["POST"])
        self.add_api_route(path="/new-user", endpoint=self.POST_new_user, response_model=msg.ExtRespMsg, methods=["POST"])
        # list of default endpoints for all child Router class-objects                              -   ENDED   -

    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------

    async def POST_login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        """=== Method name: POST_login_for_access_token ===================================  
        Endpoint to request access token. Use form to send necessary data.
        :param form_data:  
        :return:  
        ================================================================= by Sziller ==="""
        user = authenticate_user(self.db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"})
        access_toke_expires = timedelta(minutes=int(AUTH_TOKEN_EXPIRE_MINS))
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_toke_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    
    async def POST_new_user(self, new_usr: UserInDB = Depends(), current_user: UserInDB = Depends(get_current_active_user)):
        """=== Method name: POST_new_user =================================================  
        Endpoint to add new user to Auth-DB..
        :param current_user:  
        :return:  
        ================================================================= by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        
        # 111111 = 63
        # 000001 => use                     (0)
        # 001000 => ...
        # 010000 => engine-cust
        # 100000 => add-remove-users        (5)
        
        # 011111 => powerful user who cannot add/remove users
        
        if check_authorization(current_user.auth_code, 5):
            loc_session = SQLi.createSession(db_fullname=self.db_fullname_shmc,
                                             style=self.db_style,
                                             tables=None)
            SQLi.ADD_rows_to_table(primary_key="username", data_list=[new_usr.__dict__],
                                   row_obj=sqlUser,
                                   session=loc_session)
            loc_session.close()
        else:
            credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                 detail="Current User cannot add/remove new Users!",
                                                 headers={"WWW-Authenticate": "Bearer"})
            raise credential_exception
        return msg.ExtRespMsg()
        
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
