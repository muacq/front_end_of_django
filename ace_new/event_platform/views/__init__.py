import threading

from .views_event import *
from .views_user import *
from .views_chat import *
from .views_tag import *
from .views_user_action import *
from .test import *
from .views_register import *
from ..models import *
from ..encoder import *
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import AnonymousUser
from ..util import get_user


# def post_comment(request):
#     if '_token' not in request.POST or 'aid' not in request.POST or 'content' not in request.POST:
#         return JsonResponse({
#             'code': 0,
#             'msg': 'invalid request'
#         }, status=400)

#     user = get_user(request)
#     if isinstance(user, AnonymousUser):
#         return JsonResponse({
#             'code': 0,
#             'msg': 'You need to log in to post comment'
#         }, status=400)

#     event = Event.objects.get(pk=request.POST['aid'])
#     comment = Comment(poster=user, target_event=event, content=request.POST['content'])
#     comment.save()
#     return JsonResponse({
#         'code': 1,
#         'msg': 'success'
#     })


class EmailThread(threading.Thread):  # TODO: move to util.py
    def __init__(self, subject, content, receiver_list):
        self.subject = subject
        self.content = content
        self.receiver_list = receiver_list
        super(EmailThread, self).__init__()

    def run(self):
        # context = {
        #     'team': self.team,
        #     'members': self.team.member_set.all(),
        # }
        # content = render_to_string('form/team_email.html', context)
        email = EmailMessage(
            subject=self.subject,
            body=self.content,
            to=self.receiver_list,
            # cc=['']
        )
        # email.content_subtype = "html"
        email.send(fail_silently=False)


def post_feedback(request):
    feedback_content = request.POST['content']
    EmailThread(
        subject='feedback from user',
        content=feedback_content,
        receiver_list=['royl8@qq.com']
    ).start()

    return JsonResponse({
        'code': 1,
        'msg': 'feedback sent successfully'
    }, status=200)


def get_recommended_events(request):
    return HttpResponse(status=200)


def book_event(request):
    if 'aid' not in request.POST or '_token' not in request.POST or 'type' not in request.POST:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    user = get_user(request)
    event = Event.objects.get(pk=request.POST['aid'])
    if request.POST['type'] == '1':
        event.participants.add(user)
    elif request.POST['type'] == '2':
        event.followers.add(user)
    else:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    return JsonResponse({
        'code': 1,
        'msg': 'success'
    })


def get_booked_events(request):
    if '_token' not in request.POST or 'type' not in request.POST:
        return response_of_failure("missing field(s)")
    user = get_user(request)
    if request.POST['type'] == '1':
        events = user.participated_event_set.all()
    elif request.POST['type'] == '2':
        events = user.bookmarked_event_set.all()
    else:
        return response_of_failure("invalid request")
    return JsonResponse({
        'code': 1,
        'msg': 'success',
        'info': list(events)
    }, encoder=EventSummaryEncoder)



def get_published_events(request):
    if '_token' not in request.POST or 'page' not in request.POST:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    user = get_user(request)
    events = Event.objects.filter(poster=user)
    return JsonResponse({
        'code': 1,
        'msg': 'success',
        'info': list(events)
    }, encoder=EventSummaryEncoder)


def upload_image(request):
    if 'filename' not in request.FILES:
        return response_of_failure(msg='missing field(s)')
    uploaded_image = UploadedImage(image=request.FILES['filename'])
    uploaded_image.save()
    return JsonResponse(api_returned_object(info=uploaded_image.image_url))






