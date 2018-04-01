from ..models import *
from ..encoder import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import Q
from django.db.models import Count

from datetime import datetime

from ..response_helper import AceResponseError, ace_response, encode_response


# def get_comments(request):
#     if 'aid' in request.POST:
#         event = Event.objects.get(pk=request.POST['aid'])
#         comments = list(event.comment_set.all())
#         return JsonResponse(api_returned_object(info=comments), encoder=CommentEncoder)
#     return response_of_failure(msg='Event ID not given')


# def get_my_comments(request):
#     if '_token' not in request.POST:
#         return response_of_failure(msg='Invalid token')

#     user = get_user(request)
#     if isinstance(user, AnonymousUser):
#         return response_of_failure(msg='You need to log in to view your comments.')

#     my_comments = Comment.objects.filter(poster=user)
#     return JsonResponse(api_returned_object(info=list(my_comments)), encoder=CommentEncoder)


# def update_system_config(request):
#     if '_token' not in request.POST:
#         return response_of_failure(msg='Invalid token')

#     user = get_user(request)
#     if isinstance(user, AnonymousUser):
#         return response_of_failure(msg='You need to log in to update your preferences.')

#     recommend = request.POST.get('recommend', None)
#     if recommend not in ['1', '2', '3', '4']:
#         return response_of_failure(msg='Invalid setting value')
#     notify = request.POST.get('notify', None)
#     if notify not in ['1', '2']:
#         return response_of_failure(msg='Invalid setting value')
#     receive = request.POST.get('receive', None)
#     if receive not in ['1']:
#         return response_of_failure(msg='Invalid setting value')

#     system_config = SystemConfig.objects.filter(target_user=user).first()
#     if not system_config:
#         system_config = SystemConfig(target_user=user, recommend=recommend, notify=notify, receive=receive)
#         system_config.save()
#         return JsonResponse({
#             'code': 1,
#             'msg': 'Success'
#         })

#     if recommend:
#         system_config.recommend = recommend
#     if notify:
#         system_config.notify = notify
#     if receive:
#         system_config.receive = receive
#     system_config.save()
#     return JsonResponse({
#         'code': 1,
#         'msg': 'Success'
#     })


# def get_events(request):
#     page = 1
#     event_type = None
#     search_key = None

#     if 'type' in request.POST:
#         event_type_id = request.POST['type']
#         event_type = EventType.objects.get(pk=event_type_id)
#     if 'search' in request.POST:
#         search_key = request.POST['search']

#     events = Event.objects.all()
#     if event_type is not None:
#         events = events.filter(event_type=event_type)
#     if search_key is not None:
#         events = events.filter(Q(title__icontains=search_key) | Q(description__icontains=search_key))

#     return JsonResponse(api_returned_object(info=list(events)), encoder=EventSummaryEncoder)


# def add_event(request):
#     if '_token' not in request.POST:
#         return response_of_failure(msg='Invalid token')

#     user = get_user(request)
#     if isinstance(user, AnonymousUser):
#         return response_of_failure(msg='You need to log in to post an event.')

#     required_keys = ['title', 'type', 'time_type', 'desrc', 'hour_start', 'hour_end', 'begin_time']
#     if not all([field in request.POST for field in required_keys]):
#         return response_of_failure(msg='Invalid event')

#     all_keys = ['type', 'title', 'img', 'content', 'desrc', 'add', 'question', 'time_type', 'week']

#     begin_time = request.POST['begin_time']
#     hour_start = request.POST['hour_start']
#     hour_end = request.POST['hour_end']

#     datetime_format = '%Y %A,%d %b %I:%M %p'
#     year_str = str(datetime.now().year)
#     start_time = datetime.strptime(year_str + ' ' + begin_time + ' ' + hour_start, datetime_format)
#     end_time = datetime.strptime(year_str + ' ' + begin_time + ' ' + hour_end, datetime_format)

#     new_event = Event()
#     for key in all_keys:
#         value = request.POST.get(key, None)
#         setattr(new_event, key, value)

#     new_event.start_time = start_time
#     new_event.end_time = end_time

#     import pdb; pdb.set_trace()
#     new_event.save()

# # <QueryDict: {'question[]': ['jdkdks'], 'hour_end': ['3:55 AM'], 'begin_time': ['Tuesday,22 Jan'],
# # '_token': ['a2ukqjvoxyj43bgptl1vkm47nfjpk3ka'], 'add': ['ksskks'], 'desrc': ['kdkdksk'],
# # 'week': ['Tuesday'], 'title': ['jdkdks'], 'hour_start': ['2:55 AM'], 'type': ['1'],
# # 'img': ['/media/uid_1_event_2018012225537AM.jpg'], 'time_type': ['1']}>


# def delete_event(request):
#     user = get_user(request)
#     event_id = request.POST['aid']
#     try:
#         event = Event.objects.get(pk=event_id)
#         event.delete()
#         return JsonResponse({
#             'code': 1,
#             'msg': 'Success'
#         })
#     except ObjectDoesNotExist:
#         return response_of_failure(msg='event cannot be found')


# def get_event(request):
#     event_id = request.POST['aid']
#     try:
#         event = Event.objects.get(pk=event_id)
#         return JsonResponse({
#             'code': 1,
#             'msg': '',
#             'info': event
#         }, encoder=EventDetailEncoder)
#     except ObjectDoesNotExist:
#         return response_of_failure(msg='event cannot be found')


# def get_event_types(request):
#     event_types = list(EventType.objects.all())
#     response = []
#     for event_type in event_types:
#         response.append({
#             'id': event_type.pk,
#             'name': event_type.name,
#             'img': 'https://www.newstatesman.com/sites/all/themes/creative-responsive-theme/images/new_statesman_events.jpg'
#         })
#     return JsonResponse(api_returned_object(info=response))



#################################################################################

# Question
@ace_response
def get_question(request):
    if 'id' not in request.POST:
        raise AceResponseError('Question id not specified.')
    qid = request.POST['id']
    try:
        question = Question.objects.get(pk=qid)
        return encode_response(question, QuestionDetailEncoder)
    except ObjectDoesNotExist:
        raise AceResponseError('Question cannot be found.')


@ace_response
def get_questions(request):
    offset = get_integer_value(request, 'offset', 0)
    limit = get_integer_value(request, 'limit', 5)
    print(str(offset) + " " + str(limit))
    questions = Question.objects.all()[offset:offset+limit]
    return encode_response(questions, QuestionDetailEncoder)


@ace_response
def get_recommended_questions(request):
    user = get_validated_user(request)
    tags = user.interested_tags.all()
    questions_count_tuple_list = [(question,
             len(set(tags) & set(list(question.tags.all()))))
             for question in Question.objects.all()]
    questions_count_tuple_list = [tpl for tpl in questions_count_tuple_list if tpl[1] > 0]
    questions_count_tuple_list = sorted(questions_count_tuple_list, key=lambda x: x[1], reverse=True)
    questions_list = [tpl[0] for tpl in questions_count_tuple_list]
    return encode_response(questions_list, QuestionSummaryEncoder)


@ace_response
def post_question(request):
    user = get_validated_user(request)

    if 'title' not in request.POST or 'content' not in request.POST:
        raise AceResponseError('Invalid question.')

    tags_list = get_list_value(request, 'tags', default=[])
    tags = Tag.objects.filter(pk__in=tags_list)

    title = request.POST['title']
    content = request.POST['content']
    question = Question(title=title, content=content, poster=user)
    question.save()
    question.tags.set(tags)


@ace_response
def search_questions(request):
    if 'keyword' not in request.POST:
        raise AceResponseError('Keyword not provided.')

    keyword = request.POST['keyword']
    questions = Question.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))

    return encode_response(questions, QuestionSummaryEncoder)


# Answer
@ace_response
def get_answers(request):
    if 'qid' not in request.POST:
        raise AceResponseError('Question id not specified.')
    qid = request.POST['qid']
    offset = get_integer_value(request, 'offset', 0)
    limit = get_integer_value(request, 'limit', 5)

    try:
        question = Question.objects.get(pk=qid)
        answers = Answer.objects.filter(parent_question=question)[offset:offset+limit]
        return encode_response(answers, AnswerDetailEncoder)
    except ObjectDoesNotExist:
        raise AceResponseError('Question cannot be found.')


@ace_response
def get_answer(request):
    if 'id' not in request.POST:
        raise AceResponseError('Answer id not specified.')
    aid = request.POST['id']
    try:
        answer = Answer.objects.get(pk=aid)
        return encode_response(answer, AnswerDetailEncoder)
    except ObjectDoesNotExist:
        raise AceResponseError('Answer cannot be found.')


@ace_response
def answer_question(request):
    user = get_validated_user(request)

    if 'qid' not in request.POST:
        raise AceResponseError('Question id not specified.')
    if 'content' not in request.POST:
        raise AceResponseError('Content not specified.')

    qid = request.POST['qid']
    try:
        question = Question.objects.get(pk=qid)
        content = request.POST['content']
        answer = Answer(content=content, poster=user, parent_question=question)
        answer.save()
    except ObjectDoesNotExist:
        raise AceResponseError('Question cannot be found.')


@ace_response
def has_answer(request):
    user = get_validated_user(request)
    if 'qid' not in request.POST:
        raise AceResponseError('Question id not specified.')
    qid = request.POST['qid']

    try:
        question = Question.objects.get(pk=qid)
        answers = Answer.objects.filter(parent_question=question)[:]
        for i in answers:
            if i.poster_id == user.id:
                return True
        return False
    except ObjectDoesNotExist:
        raise AceResponseError('Question cannot be found.')


# Comment
@ace_response
def get_comments(request):
    _, post_type, target_id = get_post(request)
    offset = get_integer_value(request, 'offset', 0)
    limit = get_integer_value(request, 'limit', 5)

    comments = Comment.objects.filter(comment_type=post_type, target_id=target_id)[offset:offset+limit]
    return encode_response(comments, CommentSummaryEncoder)


@ace_response
def get_comment(request):
    if 'id' not in request.POST:
        raise AceResponseError('Comment id not specified.')
    cid = request.POST['id']
    try:
        comment = Comment.objects.get(pk=cid)
        return encode_response(comment, CommentDetailEncoder)
    except ObjectDoesNotExist:
        raise AceResponseError('Comment cannot be found.')


@ace_response
def post_comment(request):
    user = get_validated_user(request)

    if 'content' not in request.POST:
        raise AceResponseError('Invalid content.')

    _, comment_type, target_id = get_post(request)
    content = request.POST['content']

    comment = Comment(comment_type=comment_type, target_id=target_id, content=content, poster=user)
    comment.save()


# Like
@ace_response
def like_post(request):
    user = get_validated_user(request)
    posts, _, _ = get_post(request)
    post = posts[0]

    if user in post.liked_users.all():
        raise AceResponseError('You already liked this post!')

    if user in post.disliked_users.all():
        raise AceResponseError('You already disliked this post!')

    post.liked_users.add(user)
    post.save()



@ace_response
def unlike_post(request):
    user = get_validated_user(request)
    posts, _, _ = get_post(request)
    post = posts[0]

    if user not in post.liked_users.all():
        raise AceResponseError('You have not liked this post!')

    post.liked_users.remove(user)
    post.save()


@ace_response
def dislike_post(request):
    user = get_validated_user(request)
    posts, _, _ = get_post(request)
    post = posts[0]

    if user in post.liked_users.all():
        raise AceResponseError('You already liked this post!')

    if user in post.disliked_users.all():
        raise AceResponseError('You already disliked this post!')

    post.disliked_users.add(user)
    post.save()


@ace_response
def undislike_post(request):
    user = get_validated_user(request)
    posts, _, _ = get_post(request)
    post = posts[0]

    if user not in post.disliked_users.all():
        raise AceResponseError('You have not disliked this post!')

    post.disliked_users.remove(user)
    post.save()


@ace_response
def has_like(request):
    user = get_validated_user(request)
    posts, _, _ = get_post(request)
    post = posts[0]

    if user in post.liked_users.all():
        return True
    return False


@ace_response
def has_dislike(request):
    user = get_validated_user(request)
    posts, _, _ = get_post(request)
    post = posts[0]

    if user in post.disliked_users.all():
        return True
    return False


# Invitation
@ace_response
def invite_user_to_answer_qestion(request):
    user = get_validated_user(request)

    if 'target_uid' not in request.POST:
        raise AceResponseError('Target user not specified.')

    if 'target_qid' not in request.POST:
        raise AceResponseError('Target question not specified.')

    target_uid = request.POST['target_uid']
    target_qid = request.POST['target_qid']
    target_user = None
    target_question = None

    try:
        target_user = User.objects.get(pk=target_uid)
        target_question = Question.objects.get(pk=target_qid)
    except ObjectDoesNotExist:
        raise AceResponseError('Target does not exist.')

    invitation = InvitationToAnswer(inviting_user=user, invited_user=target_user, target_question=target_question)
    try:
        invitation.save()
    except IntegrityError:
        raise AceResponseError('You have already invited this user to answer this question.')


@ace_response
def decline_invitation(request):
    user = get_validated_user(request)

    if 'invitation_id' not in request.POST:
        raise AceResponseError('Invitation not specified.')

    invitation_id = request.POST['invitation_id']
    invitation = None

    try:
        invitation = InvitationToAnswer.objects.get(pk=invitation_id)
    except ObjectDoesNotExist:
        raise AceResponseError('Invitation does not exist.')

    invitation.is_declined = True
    invitation.save()


@ace_response
def get_invitations(request):
    user = get_validated_user(request)

    invitations = InvitationToAnswer.objects.filter(invited_user=user, is_declined=False)
    return encode_response(invitations, encoder=InvitationToAnswerEncoder)


## Help Methods
def get_post(request):
    '''Returns post, post_type, post_id'''
    if 'post_type' not in request.POST or 'target_id' not in request.POST:
        raise AceResponseError('Invalid target.')

    post_type = request.POST['post_type']
    post_id = request.POST['target_id']

    target_class_mapping = {'1': Question, '2': Answer, '3': Comment}
    if post_type not in target_class_mapping:
        raise AceResponseError('Invalid comment type')

    target_class = target_class_mapping[post_type]

    posts = target_class.objects.filter(pk=post_id)
    if not posts:
        raise AceResponseError('Post cannot be found.')

    return posts, post_type, post_id
