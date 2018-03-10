from django.contrib import admin
from .models import User, Question, Comment, Answer, InvitationToAnswer, MatchRequest, Tag
from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email_address', 'is_superuser', 'is_staff']
    list_filter = ['id', 'is_superuser', 'is_staff']
    search_fields = ['id', 'username', 'email_address']
    filter_horizontal = ['groups', 'user_permissions', 'following_users']

class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'poster', 'tags_list']

class AnswerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'content', 'poster']

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'poster']

class InvitationToAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'inviting_user', 'invited_user', 'target_question']

class MatchRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'mentor', 'mentee']

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'tag_type_str']


admin.site.register(Session, SessionAdmin)

admin.site.register(User, UserModelAdmin)
admin.site.register(Question, QuestionModelAdmin)
admin.site.register(Answer, AnswerModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(InvitationToAnswer, InvitationToAnswerAdmin)
admin.site.register(MatchRequest, MatchRequestAdmin)
admin.site.register(Tag, TagAdmin)
