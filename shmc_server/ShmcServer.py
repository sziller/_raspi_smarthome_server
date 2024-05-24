from fastapi import FastAPI


class Server(FastAPI):
    def __init__(self):
        super().__init__()
        # READ BASIC SETTINGS                                                                   -   START   -
        # from .env:
        load_dotenv()
        # Mount settings:
        mount_script: str = os.getenv("PATH_MOUNTSHARES")
        # DB settings:
        session_name_shmc: str = os.getenv("DB_FULLNAME_SHMC")
        session_style_shmc: str = os.getenv("DB_STYLE_SHMC")
        session_name_auth: str = os.getenv("DB_FULLNAME_AUTH")
        session_style_auth: str = os.getenv("DB_STYLE_AUTH")
        # from config.py:
        # language settings:
        LNG: str = conf.LANGUAGE_CODE
        # path settings:
        fsh_dir_info: str = conf.NECESSARY_DIRECTORIES
        root_path: str = conf.PATH_ROOT
        err_msg_path: str = conf.PATH_ERROR_MSG.format(root_path)
        app_inf_path: str = conf.PATH_APP_INFO.format(root_path)
        mount_from: str = conf.PATH_STATIC_FROM
        mount_to: str = conf.PATH_STATIC_TO
        # log settings:
        log_format: str = conf.LOG_FORMAT
        log_level: str = getattr(logging, conf.LOG_LEVEL)
        log_ts: str = "_{}".format(TiFo.timestamp()) if conf.LOG_TIMED else ""
        log_tf: str = conf.LOG_TIMEFORMAT
        log_filename: str = conf.LOG_FILENAME.format(root_path, log_ts)
        # app settings:
        app_id: str = conf.APP_ID
        # READ BASIC SETTINGS                                                                   -   ENDED   -
    pass
    
