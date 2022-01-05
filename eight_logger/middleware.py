import json
import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from .main import Logger

User = get_user_model()

BASE_META_ATTRIBUTES = [
    "HTTP_USERNAME",
    "REQUEST_METHOD",
    "QUERY_STRING",
    "CONTENT_TYPE",
    "CONTENT_LENGTH",
    "HTTP_REFERER",
    "REMOTE_HOST",
    "REMOTE_ADDR",
    "HTTP_AUTHORIZATION",
    "HTTP_HOST",
    "HTTP_CONNECTION",
    "HTTP_ACCEPT",
    "HTTP_USER_AGENT",
    " HTTP_SEC_FETCH_MODE",
    "HTTP_SEC_FETCH_SITE",
    "HTTP_ACCEPT_ENCODING",
    "HTTP_ACCEPT_LANGUAGE",
    "GATEWAY_INTERFACE",
    "SERVER_PROTOCOL",
    "wsgi.url_scheme",
    "wsgi.multithread",
    "wsgi.multiprocess",
    "SERVER_PORT",
    "SERVER_NAME",
    "PATH_INFO",
    "SERVER_SOFTWARE",
]

logger = Logger()

EXCLUDE_ROUTES = settings.EIGHTLAB_LOGGER["EXCLUDE_ROUTES"]


class LoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super(LoggingMiddleware, self).__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        meta = request.META
        x = [x for x in BASE_META_ATTRIBUTES if x not in meta]
        other_metadata_attributes = [x for x in BASE_META_ATTRIBUTES if x in meta]
        other_metadata_key = list(
            set(other_metadata_attributes)
            - set(["wsgi.input", "wsgi.errors", "wsgi.file_wrapper"])
        )  # excluded becasue they are file like object
        other_metadata_value = [meta[x] for x in other_metadata_key]
        metadata_json_dump = json.dumps(
            dict(zip(other_metadata_key, other_metadata_value))
        )
        metadata_json_dump = json.loads(metadata_json_dump.replace("\\", ""))
        path_info = meta["PATH_INFO"]
        r = [x for x in EXCLUDE_ROUTES if path_info.startswith(x)]
        if not r:
            username = request.user.username if request.user else None
            if not username:
                username = meta.get(BASE_META_ATTRIBUTES[0], "")
            request_method = meta.get(BASE_META_ATTRIBUTES[1], "")
            request_query_string = meta.get(BASE_META_ATTRIBUTES[2], "")
            request_payload = request.body
            try:
                request_payload = request_payload.decode("utf-8")
            except Exception as e:
                request_payload = None

            request_url = (
                    meta.get("wsgi.url_scheme", "")
                    + "://"
                    + meta.get("SERVER_NAME", "")
                    + ":"
                    + meta.get("SERVER_PORT", "")
                    + meta.get("PATH_INFO", "")
            )
            request_content_type = meta.get(BASE_META_ATTRIBUTES[3], "")
            request_content_length = meta.get(BASE_META_ATTRIBUTES[4], "")
            request_referer_url = meta.get(BASE_META_ATTRIBUTES[5], "")
            request_user_host = meta.get(BASE_META_ATTRIBUTES[6], "")
            request_user_ip = meta.get(BASE_META_ATTRIBUTES[7], "")
            request_user_authorization = meta.get(BASE_META_ATTRIBUTES[8], "")
            request_user_hostheader = meta.get(BASE_META_ATTRIBUTES[9], "")
            http_connection = meta.get(BASE_META_ATTRIBUTES[10], "")
            http_accept = meta.get(BASE_META_ATTRIBUTES[11], "")
            user_agent = meta.get(BASE_META_ATTRIBUTES[12], "")
            sec_fetch_mode = meta.get(BASE_META_ATTRIBUTES[13], "")
            sec_fetch_site = meta.get(BASE_META_ATTRIBUTES[14], "")
            accept_encoding = meta.get(BASE_META_ATTRIBUTES[15], "")
            accept_lang = meta.get(BASE_META_ATTRIBUTES[16], "")
            gateway_interface = meta.get(BASE_META_ATTRIBUTES[17], "")
            server_protocol = meta.get(BASE_META_ATTRIBUTES[18], "")
            wsgi_url_scheme = meta.get(BASE_META_ATTRIBUTES[19], "")
            wsgi_multithread = meta.get(BASE_META_ATTRIBUTES[20], "")
            wsgi_multiprocess = meta.get(BASE_META_ATTRIBUTES[21], "")
            user_server_port = meta.get(BASE_META_ATTRIBUTES[22], "")
            user_server_name = meta.get(BASE_META_ATTRIBUTES[23], "")
            user_path_info = meta.get(BASE_META_ATTRIBUTES[24], "")
            server_software = meta.get(BASE_META_ATTRIBUTES[25], "")

            json_data = {
                "username": username,
                "request_content_length": request_content_length,
                "request_content_type": request_content_type,
                "request_method": request_method,
                "request_payload": request_payload,
                "request_query_string": request_query_string,
                "request_referer_url": request_referer_url,
                "request_url": request_url,
                "request_user_authorization": request_user_authorization,
                "request_user_host": request_user_host,
                "http_connection": http_connection,
                "http_accept": http_accept,
                "user_agent": user_agent,
                "sec_fetch_mode": sec_fetch_mode,
                "sec_fetch_site": sec_fetch_site,
                "accept_encoding": accept_encoding,
                "accept_lang": accept_lang,
                "gateway_interface": gateway_interface,
                "server_protocol": server_protocol,
                "wsgi_url_scheme": wsgi_url_scheme,
                "wsgi_multithread": wsgi_multithread,
                "wsgi_multiprocess": wsgi_multiprocess,
                "user_server_port": user_server_port,
                "user_server_name": user_server_name,
                "user_path_info": user_path_info,
                "server_software": server_software,
                "other_metadata": metadata_json_dump,
            }

            user_id = None

            if username:
                user_id = User.objects.get(username=username).id
            # save the access log
            logger.access(request_method, user_id, username, json_data)


    def process_exception(self, request, exception):
        logger.exception("traceback: {}".format(traceback.format_exc()))
        return None
