from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    # User
    url(r'^api/login/register$', views.user_register),

    url(r'^api/login/login$', views.user_login),

    url(r'^api/follow/follow$', views.follow_user),

    url(r'^api/follow/unfollow$', views.unfollow_user),

    url(r'^api/follow/get_followers$', views.get_followers),

    url(r'^api/follow/get_following_users$', views.get_following_users),

    url(r'^api/match/request/send$', views.send_match_request),

    url(r'^api/match/request/get_received$', views.get_match_requests_received),

    url(r'^api/match/request/accept$', views.accept_match_request),

    url(r'^api/match/request/decline$', views.decline_match_request),

    url(r'^api/match/check_status$', views.check_match_status),

    url(r'^api/match/get_mentors$', views.get_mentors),

    url(r'^api/match/get_mentees$', views.get_mentees),

    url(r'^api/match/break_match$', views.break_match),

    # Question
    url(r'^api/question/get_questions$', views.get_questions),

    url(r'^api/question/get_recommended$', views.get_recommended_questions),

    url(r'^api/question/get_question$', views.get_question),

    url(r'^api/question/post_question$', views.post_question),

    url(r'^api/question/search_questions$', views.search_questions),

    url(r'^api/question/invitation/invite$', views.invite_user_to_answer_qestion),

    url(r'^api/question/invitation/decline$', views.decline_invitation),

    url(r'^api/question/invitation/invitations$', views.get_invitations),

    url(r'^api/question/tag_question$', views.tag_question),

    # Answer
    url(r'^api/question/get_answers$', views.get_answers),

    url(r'^api/question/get_answer$', views.get_answer),

    url(r'^api/question/answer_question$', views.answer_question),

    # Comment
    url(r'^api/question/get_comments$', views.get_comments),

    url(r'^api/question/get_comment$', views.get_comment),

    url(r'^api/question/post_comment$', views.post_comment),

    # Like
    url(r'^api/question/like_post$', views.like_post),

    url(r'^api/question/unlike_post$', views.unlike_post),

    url(r'^api/question/dislike_post$', views.dislike_post),

    url(r'^api/question/undislike_post$', views.undislike_post),

    # Tag
    url(r'^api/tags/query$', views.query_tags),

    url(r'^api/tags/add$', views.add_tag),

    url(r'^api/tags/interest/update$', views.update_interest),

    url(r'^api/tags/interest/get$', views.get_interests),

    url(r'^register/$',views.register)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

