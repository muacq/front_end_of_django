import json

from .models import *
from django.contrib.auth.models import AnonymousUser
from importlib import import_module
from django.conf import settings
from django.utils.module_loading import import_string
from django.http import JsonResponse
from .response_helper import AceResponseError

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def load_backend(path):
    return import_string(path)()


def get_user(request):
    session = None
    if '_token' in request.POST:
        session = SessionStore(session_key=request.POST['_token'])
    elif '_token' in request.GET:
        session = SessionStore(session_key=request.GET['_token'])
    if session is None:
        return AnonymousUser()
    if not session.keys():
        return AnonymousUser()

    user_id = session['_auth_user_id']
    backend_path = session['_auth_user_backend']

    if backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        user = backend.get_user(user_id)
        # TODO: Verify the session

    return user or AnonymousUser()


def get_validated_user(request):
    if '_token' not in request.POST:
        raise AceResponseError('Invalid token')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        raise AceResponseError('You need to log in.')

    return user


def get_integer_value(request, key, default=None):
    if key not in request.POST:
        if default:
            return default
        raise AceResponseError('No {} value provided.'.format(key))
    try:
        return int(request.POST[key])
    except ValueError:
        if default:
            return default
        raise AceResponseError('Invalid {} value.'.format(key))


def get_list_value(request, key, default=None):
    if key not in request.POST:
        if default:
            return default
        raise AceResponseError('No {} value provided.'.format(key))
    new_interests = None
    try:
        new_interests = json.loads(request.POST.get(key, default))
    except json.decoder.JSONDecodeError:
        if default:
            return default
        raise AceResponseError('Invalid {} value.'.format(key))

    if not isinstance(new_interests, list):
        if default:
            return default
        raise AceResponseError('Invalid {} value.'.format(key))

    return new_interests
