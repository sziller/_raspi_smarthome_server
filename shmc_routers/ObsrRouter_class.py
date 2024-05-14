import os
import zmq
import time
import logging
import inspect
from shmc_routers._ShmcBaseRouter import ShmcBaseRouter
from shmc_messages import msg
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "d4846a50fd0f03bca8e65e26672172d4436a9ab3d43ecada1d90a17acf25dfd9"
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

temp_db = {"sziller": {"username": "sziller",
                   "full_name": "Sziller",
                   "email": "szillerke@gmail.com",
                   "hashed_psswd": "$2b$12$y89rEEomoa3gS7fwir7n8O3y9JETU/adO6GC6wI5TEM22SR5w5j3e",
                   "disabled": False}}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None   = None


class User(BaseModel):
    username: str
    email: str or None      = None
    full_name: str or None  = None
    disabled: bool or None  = None


class UserInDB(User):
    hashed_psswd: str


# Setting up logger                                                                     -   START   -
lg = logging.getLogger()
# Setting up logger                                                                     -   ENDED   -

def fake_decode_token(token):
    return {"username": token, "scope": "fake"}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="obsr/token")

def verify_psswd(plain_psswd, hashed_psswd):
    return pwd_context.verify(plain_psswd, hashed_psswd)
    
def get_psswd_hash(psswd):
    return pwd_context.hash(psswd)

def get_usr(db, username):
    if username in temp_db:
        usr_data = db[username]
        return UserInDB(**usr_data)
    
def authenticate_user(db, username, psswd):
    usr = get_usr(db = temp_db, username=username)
    if not usr:
        return False
    if not verify_psswd(psswd, usr.hashed_psswd):
        return False
    return usr

def create_access_token(data: dict, expires_delta: (timedelta, None) = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldnt validate",
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_usr(db=temp_db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user
    
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



class ObsrRouter(ShmcBaseRouter):
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
        self.name: str                  = name
        self.alias: str                 = alias
        self.ip: str                    = ip            # ip of remote Engine and Message handler (zmq socket endpoint)
        self.port: int                  = port          # port remote server runs on - for DB communication
        self.zmq_port: int              = zmq_port      # port of remote Message handler (zmq socket endpoint)
        self.db_fullname: (str, None)   = db_fullname
        self.db_style: (str, None)      = db_style

        self.add_api_route("/v0/send-message/", self.GET_send_message,  methods=["GET"])
        self.add_api_route("/v0/photo/",        self.GET_photo,         methods=["GET"])
        
        self.add_api_route("/token", self.login_for_access_token, response_model=Token, methods=["POST"])

    # list of default endpoints for all child Router class-objects                              -   START   -

    # list of default endpoints for all child Router class-objects                              -   ENDED   -

    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   START   -
    # ---------------------------------------------------------------------------------------------------------------
    
    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(temp_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"})
        access_toke_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_toke_expires)
        return {"access_token": access_token, "token_type": "Bearer"}
    
    async def GET_send_message(self, message: str):
        """=== Function name: GET_send_message =========================================================================
        description...
    
        :param message: str -  'pins' or 'process' depending on the dynamic of the happening:
                                'pin_info' is a point in time
                                'process' is a duration
        ============================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        lg.debug("request   : {} / {:>25} says {} at {}".format(timestamp, cmn, self.ccn, os.path.basename(__file__)))
        data_dict = {"command": cmn,
                     "user_id": "sziller_dev",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {'message': message},
                     "timestamp": timestamp}
        msg_router_to_engine = msg.InternalMsg.init_by_dict(**data_dict)
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        lg.info("socket up : {}:{}".format(self.ip, self.zmq_port))
        socket.connect("tcp://{}:{}".format(self.ip, self.zmq_port))
        socket.send_pyobj(msg_router_to_engine)
        response = socket.recv_pyobj()

        socket.close()  # Close the socket after use
        context.term()  # Terminate the ZeroMQ context
        return {"message": response}

    async def GET_photo(self, current_user: dict = Depends(get_current_active_user)):
        """=== Function name: GET_photo ================================================================================
        description...
        ============================================================================================== by Sziller ==="""
        cmn = inspect.currentframe().f_code.co_name  # current method name
        timestamp = time.time()
        lg.debug("request   : {} / {:>25} says {} at {}".format(timestamp, cmn, self.ccn, os.path.basename(__file__)))
        data_dict = {"command": cmn,
                     "user_id": "sziller_dev",
                     "email": "szillerke@gmail.com",
                     "signature": b'',
                     "payload": {"teszt"},
                     "timestamp": timestamp}
        msg_router_to_engine = msg.InternalMsg.init_by_dict(**data_dict)
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        lg.info("socket up : {}:{}".format(self.ip, self.zmq_port))
        socket.connect("tcp://{}:{}".format(self.ip, self.zmq_port))
        socket.send_pyobj(msg_router_to_engine)
        response = socket.recv_pyobj()

        socket.close()  # Close the socket after use
        context.term()  # Terminate the ZeroMQ context
        return response.as_dict
    # ---------------------------------------------------------------------------------------------------------------
    # - Endpoints                                                                           Endpoints   -   ENDED   -
    # ---------------------------------------------------------------------------------------------------------------
    
    
print(get_psswd_hash("nevandhgrm"))
