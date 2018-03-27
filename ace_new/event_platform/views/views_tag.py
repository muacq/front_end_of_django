import json
from ..models import *
from ..encoder import *
from ..util import *
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from ..response_helper import AceResponseError, ace_response, encode_response



@ace_response
def query_tags(request):
    keyword = request.POST.get('keyword', None)
    tag_type = request.POST.get('tag_type', None)
    offset = get_integer_value(request, 'offset', 0)
    limit = get_integer_value(request, 'limit', 5)

    tags = Tag.objects.all()
    if tag_type:
        tags = tags.filter(tag_type=tag_type)
    if keyword:
        tags = tags.filter(name__icontains=keyword)
    tags = tags[offset:offset+limit]
    return encode_response(tags, TagEncoder)


@ace_response
def add_tag(request):
    _ = get_validated_user(request)
    if 'name' not in request.POST:
        raise AceResponseError('Invalid tag name.')

    name = request.POST['name']
    if not name:
        raise AceResponseError('Invalid tag name.')

    tag_type = get_integer_value(request, 'tag_type', 0)
    tag = Tag(name=name, tag_type=tag_type)
    try:
        tag.save()
    except IntegrityError:
        raise AceResponseError('Tag already exists.')


@ace_response
def update_interest(request):
    user = get_validated_user(request)
    if 'new_interests' not in request.POST:
        raise AceResponseError('New interests not provided')

    new_interests = get_list_value(request, 'new_interests')
    tags = Tag.objects.filter(pk__in=new_interests)
    user.interested_tags.set(tags)
    user.save()


@ace_response
def get_interests(request):
    user = get_validated_user(request)
    tags = user.interested_tags.all()
    return encode_response(tags, TagEncoder)


@ace_response
def tag_question(request):
    _ = get_validated_user(request)
    tags_list = get_list_value(request, 'tags', default=[])
    tags = Tag.objects.filter(pk__in=tags_list)
    if 'qid' not in request.POST:
        raise AceResponseError('Question ID not provided.')
    qid = request.POST['qid']
    question = None
    try:
        question = Question.objects.get(pk=qid)
    except ObjectDoesNotExist:
        raise AceResponseError('Target question not found.')

    question.tags.set(tags)


@ace_response
def get_tags_by_question(request):
    # TODO
    # _ = get_validated_user(request)
    if 'qid' not in request.POST:
        raise AceResponseError('Question ID not provided.')
    qid = request.POST['qid']
    question = None
    try:
        question = Question.objects.get(pk=qid)
    except ObjectDoesNotExist:
        raise AceResponseError('Target question not found.')
    tags = question.tags.all()
    return encode_response(tags, TagEncoder)