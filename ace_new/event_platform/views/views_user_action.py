from ..models import *
from ..encoder import *
from ..util import *
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from ..response_helper import AceResponseError, ace_response, encode_response


# Follow

@ace_response
def follow_user(request):
    user = get_validated_user(request)
    target_user = get_target_user(request)

    if target_user in user.following_users.all():
        raise AceResponseError('You have already followed this user.')

    user.following_users.add(target_user)


@ace_response
def unfollow_user(request):
    user = get_validated_user(request)
    target_user = get_target_user(request)

    if target_user not in user.following_users.all():
        raise AceResponseError('You have not followed this user.')

    user.following_users.remove(target_user)


@ace_response
def get_followers(request):
    _ = get_validated_user(request)
    target_user = get_target_user(request)

    return encode_response(target_user.follower_set.all(), UserInfoEncoder)


@ace_response
def get_following_users(request):
    _ = get_validated_user(request)
    target_user = get_target_user(request)

    return encode_response(target_user.following_users.all(), UserInfoEncoder)


# Match

@ace_response
def send_match_request(request):
    user = get_validated_user(request)
    target_user = get_target_user(request)

    match_request = MatchRequest(mentee=user, mentor=target_user)

    try:
        match_request.save()
    except IntegrityError:
        raise AceResponseError('You have already sent match request to this person.')


@ace_response
def get_match_requests_received(request):
    user = get_validated_user(request)
    match_requests = MatchRequest.objects.filter(mentor=user, is_declined=False, is_accepted=False)
    return encode_response(match_requests, MatchRequestEncoder)


@ace_response
def accept_match_request(request):
    user = get_validated_user(request)
    match_request = get_match_request(request)

    if match_request.mentor != user:
        raise AceResponseError('No permission')

    mentee = match_request.mentee
    mentee.mentors.add(user)
    mentee.save()

    match_request.is_accepted = True
    match_request.save()


@ace_response
def decline_match_request(request):
    user = get_validated_user(request)
    match_request = get_match_request(request)

    if match_request.mentor != user:
        raise AceResponseError('No permission')

    match_request.is_declined = True
    match_request.save()


@ace_response
def check_match_status(request):
    user = get_validated_user(request)
    target_user = get_target_user(request)

    relations = []

    if target_user in user.mentors.all():
        relations.append('Mentor')

    if target_user in user.mentees.all():
        relations.append('Mentee')

    if MatchRequest.objects.filter(mentee=user, mentor=target_user):
        relations.append('Match Request Sent')

    return relations


@ace_response
def get_mentors(request):
    user = get_validated_user(request)
    return encode_response(user.mentors.all(), UserInfoEncoder)


@ace_response
def get_mentees(request):
    user = get_validated_user(request)
    return encode_response(user.mentees.all(), UserInfoEncoder)


@ace_response
def break_match(request):
    user = get_validated_user(request)
    if 'is_mentee' not in request.POST:
        raise AceResponseError('Invalid is_mentee value')

    is_mentee = get_integer_value(request, 'is_mentee')
    if is_mentee not in [0, 1]:
        raise AceResponseError('Invalid is_mentee value')

    target_user = get_target_user(request)
    if is_mentee:
        if target_user in user.mentors.all():
            user.mentors.remove(target_user)
            MatchRequest.objects.get(mentee=user, mentor=target_user).delete()
        else:
            raise AceResponseError('This user is not your mentor.')
    else:
        if target_user in user.mentees.all():
            user.mentees.remove(target_user)
            MatchRequest.objects.get(mentor=user, mentee=target_user).delete()
        else:
            raise AceResponseError('This user is not your mentee.')


# Helper methods
def get_target_user(request):
    if 'target_uid' not in request.POST:
        raise AceResponseError('Invalid target user.')

    target_uid = request.POST['target_uid']
    try:
        target_user = User.objects.get(pk=target_uid)
        return target_user
    except ObjectDoesNotExist:
        raise AceResponseError('Target user cannot be found.')


def get_match_request(request):
    if 'mrid' not in request.POST:
        raise AceResponseError('Invalid match request.')

    mrid = request.POST['mrid']
    try:
        match_request = MatchRequest.objects.get(pk=mrid)
        return match_request
    except ObjectDoesNotExist:
        raise AceResponseError('Target match request cannot be found.')
