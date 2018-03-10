from .views_event import *
# from .views_user import *
from ..models import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user, login, authenticate
from django.db import IntegrityError

from ..response_helper import AceResponseError, ace_response


def _validate_email_format(email):
    return True


def _validate_password_format(password):
    return len(password) >= 6


@ace_response
def user_login(request):
    input_email_address = request.POST['email']
    input_password = request.POST['password']
    user = authenticate(email_address=input_email_address, password=input_password)
    if user is not None:
        if user.is_active:
            login(request, user)
            user_session_key = request.session.session_key
            return {
                '_token': user_session_key,
                'msg': 'login success'
            }
        else:
            raise AceResponseError('account is not active')
    else:
        raise AceResponseError('account not found')


@ace_response
def user_register(request):
    print(request)
    form = request.POST
    print(form)
    if 'email' not in form or 'username' not in form or 'password' not in form:
        raise AceResponseError('missing field(s)')
    username = form['username']
    email = form['email']
    password = form['password']

    if not _validate_email_format(email):
        raise AceResponseError('incorrect email address format')
    if not _validate_password_format(password):
        raise AceResponseError('password must contain at least 6 digits')

    try:
        new_user = User(username=username, email_address=email)
        new_user.set_password(password)
        new_user.save()
        # new_system_config = SystemConfig(target_user=new_user)
        # new_system_config.save()

        new_session = SessionStore()
        new_session.create()
        request.session = new_session
        request.session.modified = True

        login(request, new_user)
        return {
            '_token': request.session.session_key,
            'msg': 'login success'
        }
    except IntegrityError:
        raise AceResponseError('username or email already exists')


# def get_user_info(request):
#     if '_token' not in request.POST:
#         raise AceResponseError('missing field(s)')
#     user = get_user(request)
#     if isinstance(user, AnonymousUser):
#         raise AceResponseError('you need to login first')
#     return user, UserInfoEncoder


# def get_user_space(request):
#     if 'uid' not in request.POST or '_token' not in request.POST:
#         raise AceResponseError('missing field(s)')
#     user = get_user(request)
#     if isinstance(user, AnonymousUser):
#         raise AceResponseError('you need to login first')

#     try:
#         target_user = User.objects.get(pk=request.POST['uid'])
#         target_user_json = UserInfoEncoder().default(target_user)
#         target_user_json['statement'] = 'to be add'
#         target_user_json['occupation'] = 'to be add'

#         target_user_space_json = {}
#         target_user_space_json['user'] = target_user_json
#         target_user_space_json['event'] = list(target_user.participated_event_set.all())

#         if target_user in user.follower_set.all():
#             target_user_space_json['is_friend'] = '1'
#         else:
#             target_user_space_json['is_friend'] = '0'
#     except ObjectDoesNotExist:
#         raise AceResponseError('target user not found')

#     return target_user_space_json





