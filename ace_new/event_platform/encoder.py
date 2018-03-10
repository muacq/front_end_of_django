from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import AnonymousUser
from .models import *


def format_datetime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')


class UserInfoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id': obj.pk,
                'username': obj.username,
                'img': "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",
                'is_show_email': True,  # TODO: set accordingly
                'email': obj.email_address,
                'statement': 'to be add',
                'occupation': 'to be add',
                'age': '1',
                'sex': '1',
                'is_show_event': False
            }
        return super().default(obj)


# class EventSummaryEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Event):
#             return {
#                 "id": obj.pk,
#                 "aid": obj.pk,
#                 # "start_time": format_datetime(obj.start_time),
#                 # "end_time": format_datetime(obj.end_time),
#                 'week': '1',
#                 'begin_time': '2018-1-12',
#                 'hour_start': '10:12:12',
#                 'hour_end': '10:14:12',
#                 'time_type': '1',
#                 "content": "hellodhjsds",
#                 "title": obj.title,
#                 "img": "http://mainstreamevents.homestead.com/Event_Picture.jpg",
#                 "desrc": obj.description,
#                 "add": obj.address,
#                 "type": obj.event_type.pk,
#                 "t_name": obj.event_type.name
#             }
#         return super().default(obj)


# class EventDetailEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Event):
#             return {
#                 "id": obj.pk,
#                 "aid": obj.pk,
#                 # "start_time": format_datetime(obj.start_time),
#                 # "end_time": format_datetime(obj.end_time),
#                 'week': '1',
#                 'begin_time': '2018-1-12',
#                 'hour_start': '10:12:12',
#                 'hour_end': '10:14:12',
#                 'time_type': '1',
#                 "title": obj.title,
#                 "img": "http://mainstreamevents.homestead.com/Event_Picture.jpg",
#                 "desrc": obj.description,
#                 "add": obj.address,
#                 "type": obj.event_type.pk,
#                 "t_name": obj.event_type.name,
#                 "uid": obj.poster.pk,
#                 'u_img': 'https://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=85495748'
#             }
#         return super().default(obj)


# class CommentEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Comment):
#             return {
#                 "id": obj.pk,
#                 "uid": obj.poster.pk,
#                 "aid": obj.target_event.pk,
#                 "content": obj.content,
#                 "c_time": format_datetime(obj.post_time),  # "0000-00-00 00:00:00"
#                 "u_username": obj.poster.username,
#                 'u_img': 'https://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=85495748'
#             }
#         return super().default(obj)


# class FriendEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, User):
#             return {
#                 'id': obj.pk,
#                 'uid': obj.pk,
#                 'fid': obj.pk,
#                 'u_username': obj.username,
#                 'u_img': 'https://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=85495748'
#             }
#         return super().default(obj)


###########################################################################
class QuestionSummaryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            return {
                'id': obj.pk,
                'title': obj.title,
                'content': obj.content,
                'post_time': obj.post_time,
                'poster': obj.poster.username,
                'poster_id': obj.poster.id
            }
        return super().default(obj)


class QuestionDetailEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            return {
                'id': obj.pk,
                'title': obj.title,
                'content': obj.content,
                'post_time': obj.post_time,
                'poster': obj.poster.username,
                'poster_id': obj.poster.id,
                'like_count': obj.like_count,
                'dislike_count': obj.dislike_count
            }
        return super().default(obj)


class AnswerDetailEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Answer):
            return {
                'id': obj.pk,
                'content': obj.content,
                'post_time': obj.post_time,
                'poster': obj.poster.username,
                'poster_id': obj.poster.id,
                'like_count': obj.like_count,
                'dislike_count': obj.dislike_count
            }
        return super().default(obj)


class AnswerSummaryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Answer):
            return {
                'id': obj.pk,
                'content': obj.content,
                'post_time': obj.post_time,
                'poster': obj.poster.username,
                'poster_id': obj.poster.id
            }
        return super().default(obj)

class CommentDetailEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Comment):
            return {
                'id': obj.pk,
                'content': obj.content,
                'post_time': obj.post_time,
                'poster': obj.poster.username,
                'poster_id': obj.poster.id,
                'comment_type': obj.comment_type,
                'target_id': obj.target_id,
                'like_count': obj.like_count,
                'dislike_count': obj.dislike_count
            }
        return super().default(obj)


class CommentSummaryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Comment):
            return {
                'id': obj.pk,
                'content': obj.content,
                'post_time': obj.post_time,
                'poster': obj.poster.username,
                'poster_id': obj.poster.id,
                'comment_type': obj.comment_type,
                'target_id': obj.target_id
            }
        return super().default(obj)


class InvitationToAnswerEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, InvitationToAnswer):
            return {
                'id': obj.pk,
                'inviting_user': obj.inviting_user.username,
                'invited_user': obj.invited_user.username,
                'question': obj.target_question.title
            }
        return super().default(obj)


class MatchRequestEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, MatchRequest):
            return {
                'id': obj.pk,
                'mentor': obj.mentor.username,
                'mentee': obj.mentee.username,
                'mentor_id': obj.mentor.pk,
                'mentee_id': obj.mentee.pk,
            }
        return super().default(obj)


class TagEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tag):
            return {
                'id': obj.pk,
                'name': obj.name,
                'tag_type': obj.tag_type,
                'tag_type_str': obj.tag_type_str,
            }
        return super().default(obj)
