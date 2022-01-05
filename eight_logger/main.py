import json
import logging
from logging.handlers import RotatingFileHandler
import os

from django.conf import settings

from eight_logger.db_utils import (save_access_log, save_error_log, save_exception_log)
from eight_logger.settings import api_settings

"""
formatter will be used to define the format of logs in the file.
"""
formatter = logging.Formatter("%(asctime)s : [%(levelname)s] - %(message)s")


class Logger:

    def __init__(self):
        self.info_file_path = self.get_info_file_path()
        self.error_file_path = self.get_error_file_path()
        self.exception_file_path = self.get_exception_file_path()
        self.access_file_path = self.get_access_file_path()
        self.max_bytes = self.get_max_bytes()
        self.backup_count = self.get_backup_count()
        self.info_logger = self.setup_logger(
            "eightlab-info-logger", 
            self.info_file_path,
            self.max_bytes,
            self.backup_count,
            logging.INFO
        )
        self.error_logger = self.setup_logger(
            "eightlab-error-logger",
            self.error_file_path,
            self.max_bytes,
            self.backup_count,
            logging.ERROR
        )
        self.exception_logger = self.setup_logger(
            "eightlab-exception-logger",
            self.exception_file_path,
            self.max_bytes,
            self.backup_count,
            logging.ERROR
        )
        self.access_logger = self.setup_logger(
            "eightlab-access-logger",
            self.access_file_path,
            self.max_bytes,
            self.backup_count,
            logging.INFO
        )

        self.EVENT_MAPPING = {
            "GET": "retrieve",
            "POST": "add",
            "PUT": "update",
            "DELETE": "delete",
            "PATCH": "update"
        }

    def setup_logger(self, name, log_file, size=20971520, backup_count=50, level=logging.INFO):
        """
            Setup for creating logger instance of python logging module
        """
        handler = RotatingFileHandler(log_file, maxBytes=size, backupCount=backup_count)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger
    
    def get_info_file_path(self) -> str:
        """
            get file path for info level log
        """
        try:
            INFO_FILE_PATH = api_settings.INFO_LOG_FILE["PATH"]
            if not os.path.exists(INFO_FILE_PATH):
                os.mknod(INFO_FILE_PATH)
        except:
            INFO_FILE_PATH = None
        
        return INFO_FILE_PATH
    
    def get_error_file_path(self) -> str:
        """
            get file path for error level log
        """
        try:
            ERROR_FILE_PATH = api_settings.ERROR_LOG_FILE["PATH"]
            if not os.path.exists(ERROR_FILE_PATH):
                os.mknod(ERROR_FILE_PATH)
        except:
            ERROR_FILE_PATH = None

        return ERROR_FILE_PATH
    
    def get_access_file_path(self) -> str:
        """
            get file path for access level log
        """
        try:
            ACCESS_FILE_PATH = api_settings.ACCESS_LOG_FILE["PATH"]
            if not os.path.exists(ACCESS_FILE_PATH):
                os.mknod(ACCESS_FILE_PATH)
        except:
            ACCESS_FILE_PATH = None

        return ACCESS_FILE_PATH
    
    def get_exception_file_path(self) -> str:
        """
            get file path for exception level log
        """
        try:
            EXCEPTION_FILE_PATH = api_settings.EXCEPTION_LOG_FILE["PATH"]
            if not os.path.exists(EXCEPTION_FILE_PATH):
                os.mknod(EXCEPTION_FILE_PATH)
        except:
            EXCEPTION_FILE_PATH = None

        return EXCEPTION_FILE_PATH
    
    def get_max_bytes(self) -> int:
        try:
            max_bytes = api_settings.MAX_BYTES
            return 20971520
        except KeyError:
            return 20971520
    
    def get_backup_count(self) -> int:
        try:
            backup_count = api_settings.BACKUP_COUNT
            return backup_count
        except KeyError:
            return 20

    def info(self, line: str) -> None:
        self.info_logger.info(line)

    def error(self, line: str) -> None:
        self.error_logger.error(line)
        save_error_log(line)
    
    def access(
        self,
        request_method: str = None,
        user_id: int = None,
        username: str = None,
        access_log: dict = {},
        content_type_id: int = None,
        object_id: int = None,
        event: str = None,
        extra_event: str = None
    ) -> None:
        """
            saves the access json log to file.
            if manual access log is used to store specific event, the event is saved in db.
        """
        if not event:
            if request_method:
                event = self.EVENT_MAPPING.get(request_method, "")

        self.access_logger.info(
            " --- " + str(user_id) + " --- " + username + " --- " + event + ": " + json.dumps(access_log)
        )
        if content_type_id:
            """
            only save in db if content type is present
            """
            save_access_log(user_id, object_id, event, content_type_id, extra_event)
    
    def exception(self, line:str) -> None:
        self.exception_logger.error(line)
        save_exception_log(line)
