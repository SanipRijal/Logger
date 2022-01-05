"""
For example your project's `settings.py` file might look like this:

EIGHTLAB_LOGGER = {
    "EXCLUDE_ROUTES": [],
    "INFO_LOG_FILE": {
        "PATH": os.path.join(BASE_DIR, "logs/info.log"),
    },
    "ERROR_LOG_FILE": {
        "PATH": os.path.join(BASE_DIR, "logs/error.log"),
    }
}
"""
import os

from django.conf import settings
from django.utils.module_loading import import_string


DEFAULTS = {
    'EXLUDE_ROUTES': [],
    'INFO_LOG_FILE': {
        'PATH': os.path.join(settings.BASE_DIR, "logs/info.log"),
    },
    'ERROR_LOG_FILE': {
        'PATH': os.path.join(settings.BASE_DIR, "logs/error.log"),
    },
    'ACCESS_LOG_FILE': {
        'PATH': os.path.join(settings.BASE_DIR, "logs/access.log"),
    },
    'EXCEPTION_LOG_FILE': {
        'PATH': os.path.join(settings.BASE_DIR, "logs/exception.log"),
    },
    'MAX_BYTES': 20971520,
    'BACKUP_COUNT': 20,
    'EMAIL_CONFIG': {
        'SEND_MAIL': False,
        'HOST': "",
        'HOST_USER': "",
        'HOST_PASSWORD': "",
        'PORT': "",
        'DEFAULT_FROM_EMAIL': "",
        'EMAIL_TEMPLATE': "eight_logger/error.html",
        'EMAIL_FAIL_SILENTLY': True,
        'EMAIL_USE_TLS': True,
        'EMAIL_USE_PASSWORD': True,
        'EMAIL_SENDER': ""
    }
}

IMPORT_STRINGS = [
    'EXCLUDE_ROUTES',
    'INFO_LOG_FILE',
    'ERROR_LOG_FILE',
    'ACCESS_LOG_FILE',
    'EXCEPTION_LOG_FILE',
    'MAX_BYTES',
    'BACKUP_COUNT',
    'EMAIL_CONFIG'
]

REMOVED_SETTINGS = []


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val , setting_name):
    """
    Attempt to import a class from string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class APISettings:
    """
    A settings object that allows EightLab Logger settings to be accessed as properties.
    For example:
        from eight_logger.settings import api_settings
        print(api_settings.LOG_INFO_FILE)
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._chached_attrs = set()
    
    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'EIGHTLAB_LOGGER', {})
        return self._user_settings
    
    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)
        
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]
                
        if attr in self.import_strings:
            val = perform_import(val, attr)
        
        # Cache the result
        self._chached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError("The '%s' setting has been removed." % (setting))
        return user_settings


api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)
