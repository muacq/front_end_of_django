import json
import traceback
from logbook import Logger
from django.http import JsonResponse
from django.db.models.query import QuerySet

LOGGING = Logger(__name__)

class AceResponseError(Exception):
    pass

def encode_response(obj, encoder):
    enc = encoder()
    if isinstance(obj, QuerySet):
        return [enc.default(x) for x in list(obj)]
    elif isinstance(obj, list):
        return [enc.default(x) for x in obj]
    return enc.default(obj)

def ace_response(func):
    def ace_response_call(*args, **kwargs):
        status = 'OK'
        errors = []
        result = None
        try:
            result = func(*args, **kwargs)
        except AceResponseError as err:
            status = 'ERROR'
            errors.append(str(err))
        except Exception:
            LOGGING.error(traceback.format_exc())
            traceback.print_exc()
            status = 'ERROR'
            errors.append('Server Error')

        return JsonResponse({
            'result': result,
            'errors': errors,
            'status': status
        })
    return ace_response_call
