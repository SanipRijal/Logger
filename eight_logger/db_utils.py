from eight_logger.email_utils import send_email
from eight_logger.models import (AccessLog, ErrorLog, ExceptionLog)
from eight_logger.settings import api_settings


def save_access_log(user_id: int, object_id: int = None, event: str = None, content_type=None, extra_event: str = None):
    try:
        AccessLog.objects.create(
            user_id=user_id,
            object_id=object_id,
            content_type=content_type,
            event=event,
            extra_event=extra_event,
        )
    except:
        raise Exception("Cannot save access log to db.")


def save_error_log(message: str):
    try:
        ErrorLog.objects.create(message=message)
    except:
        raise Exception("Cannot save error log to db.")



def save_exception_log(message: str):
    try:
        ExceptionLog.objects.create(message=message)
        send_email(
            body={"title": "Error Occured", "body": message},
            template=api_settings.EMAIL_CONFIG.get("EMAIL_TEMPLATE", "eight_logger/error.html")
        )
    except:
        raise Exception("Cannot save exception log to db.")
