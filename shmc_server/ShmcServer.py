from fastapi import FastAPI
import os
import yaml
import uvicorn
import logging
import importlib
from fastapi.staticfiles import StaticFiles

# Setting up logger                                         logger                      -   START   -
lg = logging.getLogger()
# Setting up logger                                         logger                      -   ENDED   -


class Server:
    def __init__(self, app_id = ""):
        super().__init__()
        # READ BASIC SETTINGS                                                                   -   START   -
        # DB settings:
        self.session_name_shmc: str     = ""
        self.session_style_shmc: str    = ""
        self.session_name_auth: str     = ""
        self.session_style_auth: str    = ""
        # from config.py:
        # language settings:
        self.lng: str               = ""
        # path settings:
        self.fsh_dir_info: list     = []
        self.root_path: str         = ""
        self.err_msg_path: str      = ""
        self.app_inf_path: str      = ""
        self.mount_from: str        = ""
        self.mount_to: str          = ""
        self.srv_ip: str            = ""
        self.srv_port: int          = 0
        self.app_info: str          = ""
        # app settings:
        self.app_id: str = app_id
        self.tags_metadata: list            = []
        self.router_info: dict              = {}
        self.ERR: dict                      = {}
        self.server = FastAPI()
        self.app: FastAPI or None       = None
        
    def process(self):
        # prepare script running:                                                           -   START   -
        lg.info("setup fsh : {}".format(self.fsh_dir_info))
        self.fsh()
        lg.info("read data : from: {}".format(self.err_msg_path))
        self.ERR = self.read_yaml_data(source=self.err_msg_path)
        lg.info("read data : from: {}".format(self.app_inf_path))
        self.app_info = self.read_yaml_data(source=self.app_inf_path)
        # prepare script running:                                                           -   ENDED   -
        
        self.app = FastAPI(
            openapi_tags=self.tags_metadata,
            title=self.app_info["proj_name"],
            version=self.app_info["version"],
            summary=self.app_info["summary"],
            description=self.app_info["description"],
            contact={"name": "SmartHomeMyCastle",
                     "email": "szillerke@gmail.com"},
            terms_of_service=self.app_info["terms"],
            openapi_url=self.app_info["url"].format(self.app_info["proj_nick"]))
        self.server.mount(path="/app", app=self.app, name="shmc")
        
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
        lg.warning("mount-srvr: StaticDeta from '{}' to '{}'".format(self.mount_from, self.mount_to))

        # -------------------------------------------------------------------------------------------------------
        # StaticFiles                                                                               -   ENDED   -
        # -------------------------------------------------------------------------------------------------------
        
        self.process_server_data()
        self.process_endpoints()
        
    def process_server_data(self):
        # server data processing:                                                           -   START   -
        lg.info("read conf.: APP_ROUTER_INFO")
        lg.info("arrange   : tags_metadata")
        self.tags_metadata = []
        for name, data in self.router_info.items():
            if data["use"]:
                data["name"] = name
                self.tags_metadata.append(data)
        # server data processing:                                                           -   ENDED   -
        
    def process_endpoints(self):
        # -------------------------------------------------------------------------------------------------------------------
        # - Endpoints                                                                               Endpoints   -   START   -
        # -------------------------------------------------------------------------------------------------------------------
        ROUTER_OBJECTS = {}

        for name, data in self.router_info.items():  # looping through routing_info as key, value
            if data['use']:
                try:
                    # we import the class named: (change here to modify class name definition)
                    class_name = data['module'].split(sep=".")[1].split(sep="_")[0]
                    # we import the class from the <module>:
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
                    msg = self.ERR[103][self.lng].format(name)
                    lg.error(msg)
        lg.debug("SUMMARY   : --------------------------------------------------------------------------------")
        lg.debug("listing   : all routers included in <app> sub-server:")
        for k, v in ROUTER_OBJECTS.items():
            lg.debug("      >>> :{:>12}: {}".format(k, v))

        lg.warning("running   : SERVER from {}".format(__file__))

        # -------------------------------------------------------------------------------------------------------------------
        # - Endpoints                                                                               Endpoints   -   ENDED   -
        # -------------------------------------------------------------------------------------------------------------------

    def fsh(self):
        """=== Function name: fsh =====================================================================================
        Check and if missing create File System Hierarchy for Project
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
        """=== Function name: fsh =====================================================================================
        Check and if missing create File System Hierarchy for Project
        :return:
        ============================================================================================== by Sziller ==="""
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
        :return: 
        ========================================================================================== by Sziller ==="""
        print(self.srv_ip)
        print(self.srv_port)
        uvicorn.run(self.server, host=self.srv_ip, port=self.srv_port)
