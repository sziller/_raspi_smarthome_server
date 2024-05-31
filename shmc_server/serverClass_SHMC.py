from fastapi import FastAPI
import os
import yaml
import uvicorn
import logging
import importlib
from fastapi.staticfiles import StaticFiles
from sql_access import sql_interface as sqli
from sql_bases.sqlbase_user.sqlbase_user import User as sqlUser
from sql_access.sql_interface import createSession
from sqlalchemy.orm import Session


# Setting up logger                                         logger                      -   START   -
lg = logging.getLogger()
# Setting up logger                                         logger                      -   ENDED   -


class Server:
    """=== Classname: server ===========================================================================================
    Wrapper class to handle SHMC related server tasks
    ============================================================================================== by Sziller ==="""
    # Class parameters:                                                                     -   START   -
    # language settings:
    lng: str
    # server related parameters:
    srv_ip: str
    srv_port: int
    app_id: str
    app_path: str
    router_info: dict
    # path storage:
    fsh_dir_info: list = []
    path_root: str = ""
    path_err_msg: str = ""
    path_app_doc: str = ""
    path_mount_static_from: str = ""
    path_mount_static_to: str = ""
    # DB settings:
    session_name_shmc: str
    session_style_shmc: str
    session_name_auth: str
    session_style_auth: str
    default_user_list: list
    # Class parameters:                                                                     -   ENDED   -
    
    # AuthService:                                                                          -   START   -
    auth_service: object
    # AuthService:                                                                          -   ENDED   -
    
    def __init__(self):
        # Define instance parameters                                    -   START   -
        # auth:
        
        # classes defined
        self.server: FastAPI or None = None
        self.app: FastAPI or None = None
        
        # app settings (derived from class parameters):
        self.tags_metadata: list or None    = None
        self.app_doc: dict or None          = None
        self.err_msg: dict or None          = None
        # Define instance parameters                                    -   ENDED   -
        
    def process(self):
        """=== Method name: process ====================================================================================
        When Class is instantiated without defined parameters
        ========================================================================================== by Sziller ==="""
        # prepare script running:                                                           -   START   -
        lg.info("setup fsh : {}".format(self.fsh_dir_info))
        self.fsh()
        lg.info("read data : from: {}".format(self.path_err_msg))
        self.err_msg = self.read_yaml_data(source=self.path_err_msg)
        lg.info("read data : from: {}".format(self.path_app_doc))
        self.app_doc = self.read_yaml_data(source=self.path_app_doc)
        # prepare script running:                                                           -   ENDED   -

        lg.info("inst.ting : self.server = FastAPI()")
        self.server = FastAPI()
        lg.info("inst.ting : self.app = FastAPI() - as sub-server")
        self.app = FastAPI(
            openapi_tags=self.tags_metadata,
            title=self.app_doc["proj_name"],
            version=self.app_doc["version"],
            summary=self.app_doc["summary"],
            description=self.app_doc["description"],
            contact={"name": "SmartHomeMyCastle",
                     "email": "szillerke@gmail.com"},
            terms_of_service=self.app_doc["terms"],
            openapi_url=self.app_doc["url"].format(self.app_doc["proj_nick"]))
        lg.info("mounting  : self.app under self.server - path: {}")
        self.server.mount(path=self.app_path, app=self.app, name="shmc")
        # READ BASIC SETTINGS                                                                   -   ENDED   -

        # -------------------------------------------------------------------------------------------------------
        # StaticFiles                                                                               -   START   -
        # -------------------------------------------------------------------------------------------------------

        # ATTENTION: mounting StaticFiles over the path you use for your server, will mess up your routing-paths,
        # and "details: not found" message will indicate, you're routing is wrong."

        # path: sets the string you must type into the browser, when accessing data. You may want to "act" asif it was in a
        # subdirectory, where it isn't, or show the actual subdirectory if necessary.
        # by entering "/", you ensure the browser finds it under: host:0000/... directly
        # app contains the 'directory' parameter, which must have the actual subdirectory as an argument
        # if you call your basic page 'index.html' it can be accessed directly, without entering the actual filename

        # Route handler for the root URL
        self.server.mount(path="/", app=StaticFiles(directory="public", html=True), name="public")

        # @app.get("/")
        # async def read_index():
        #     """
        # 
        #     :return: 
        #     """
        #     # Get the path to the index.html file
        #     index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "index.html")
        #     # Check if the file exists
        #     if os.path.exists(index_path):
        #         # Return the index.html file as a response
        #         return FileResponse(index_path)
        #     else:
        #         # Return a simple message if index.html does not exist
        #         return {"message": "index.html not found"}

        # server.mount(path="/", app=StaticFiles(directory="public", html=True), name="public")
        lg.warning("mount-srvr: StaticDeta from '{}' to '{}'".format(self.path_mount_static_from, self.path_mount_static_to))

        # -------------------------------------------------------------------------------------------------------
        # StaticFiles                                                                               -   ENDED   -
        # -------------------------------------------------------------------------------------------------------
        
        self.process_server_data()
        self.process_db()
        # auth_service
        self.process_endpoints()

    def db(self, session: Session, user_list: list) -> bool:
        """

        :param session: 
        :param user_list: 
        :return: 
        """
        lg.warning("user db   : entering default users - if not included!")
        sqli.ADD_rows_to_table(primary_key="username", data_list=user_list, row_obj=sqlUser, session=session)
        return True
    
    def process_db(self):
        # server base DB session:                                                           -   START   -
        session_shmc = createSession(db_fullname=self.session_name_shmc, tables=None, style=self.session_style_shmc)
        session_auth = createSession(db_fullname=self.session_name_auth, tables=[sqlUser.__table__],
                                     style=self.session_style_auth)
        self.db(session=session_auth, user_list=self.default_user_list)
        session_shmc.close()
        session_auth.close()

        # server base DB session:                                                           -   ENDED   -
    
    def process_server_data(self):
        # server data processing:                                                           -   START   -
        lg.info("arrange   : tags_metadata")
        self.tags_metadata = []
        for name, data in self.router_info.items():
            if data["use"]:
                data["name"] = name
                self.tags_metadata.append(data)
        # server data processing:                                                           -   ENDED   -
        
    def process_endpoints(self):
        """
        
        :return: 
        """
        # -------------------------------------------------------------------------------------------------------
        # - Endpoints                                                                   Endpoints   -   START   -
        # -------------------------------------------------------------------------------------------------------
        ROUTER_OBJECTS = {}

        for name, data in self.router_info.items():  # looping through routing_info as key, value
            if data['use']:
                try:
                    # we import the class named: (change here to modify class name definition)
                    class_name = data['module'].split(sep=".")[1].split(sep="_")[0]
                    # we import the class from the <module>:
                    print(data['module'])
                    print(class_name)
                    router_class = getattr(importlib.import_module(data['module']), class_name)
                    # we instantiate it:
                    alias = data["prefix"][1:]
                    # sufix = ""
                    # if "args" in data and data["args"]["ip"] != "localhost":
                    sufix = "_" + alias.upper()
                    lg.debug("fetch args: 'alias': {}, 'sufix': {}".format(alias, sufix))
                    lg.debug("initiating: <router> from {}".format(os.path.basename(__file__)))
                    router_instance = router_class(name=name,
                                                   alias=alias,
                                                   db_fullname=os.getenv("DB_FULLNAME{}".format(sufix)),
                                                   db_style=os.getenv("DB_STYLE{}".format(sufix)))
                    # we set arguments for the instance:
                    if "args" in data and data["args"]:
                        for param, arg in data["args"].items():
                            setattr(router_instance, param, arg)
                            lg.debug("set router: '{}' - set: {} : {}".format(name, param, arg))
                        router_instance.reinit()

                    # collect instances under their names:
                    ROUTER_OBJECTS[name] = router_instance
                    lg.info("add router: {} as {}.router() - under {}".format([name], data["module"], data["prefix"]))
                    # add router instances to the <app> sub-server:
                    self.app.include_router(router=router_instance, tags=[name], prefix=data["prefix"])
                    lg.info("incl.rout.: {}".format(router_instance))
                except (ImportError, AttributeError):
                    msg = self.err_msg[103][self.lng].format(name)
                    lg.error(msg)
        lg.debug("SUMMARY   : --------------------------------------------------------------------------------")
        lg.debug("listing   : all routers included in <app> sub-server:")
        for k, v in ROUTER_OBJECTS.items():
            lg.debug("      >>> :{:>12}: {}".format(k, v))

        lg.warning("running   : SERVER from {}".format(__file__))

        # ---------------------------------------------------------------------------------------------------
        # - Endpoints                                                               Endpoints   -   ENDED   -
        # ---------------------------------------------------------------------------------------------------

    def fsh(self):
        """=== Function name: fsh =====================================================================================
        Checks and - if missing - creates File System Hierarchy for Project
        :return:
        ============================================================================================== by Sziller ==="""
        lg.debug("fsh check : Necessary FileSystemHierarchy check - START")
        for dirname in self.fsh_dir_info:
            if not os.path.exists(dirname):
                lg.warning("fsh update: New directory created: {}".format(dirname))
                os.mkdir(dirname)
        lg.debug("fsh check : Necessary FileSystemHierarchy check - ENDED")

    @staticmethod
    def read_yaml_data(source: str):
        """=== Function name: fsh ======================================================================================
        Processes yaml sourced data
        :return:
        ========================================================================================== by Sziller ==="""
        data = {"path": source, "fn": os.path.basename(__file__)}
        with open(data["path"], 'r') as stream:
            try:
                parsed_yaml = yaml.safe_load(stream)
                lg.info("prepare   : Loaded server_data from {path} - says {fn}".format(**data))
                return parsed_yaml
            except yaml.YAMLError as exc:
                lg.critical("Failed to load server_data from {path} - says {fn}".format(**data))
                raise exc
    
    def serve_forever(self):
        """=== Method name: serve_forever ==============================================================================
        Call this method to starts serving with Instance contained arguments.
        :var self.server: the Server instance we defined in current instance
        :var self.srv_ip: IP your server is accessible under
        :var self.srv_port: port your server listens on
        :return: nothing
        ========================================================================================== by Sziller ==="""
        uvicorn.run(self.server, host=self.srv_ip, port=self.srv_port)
