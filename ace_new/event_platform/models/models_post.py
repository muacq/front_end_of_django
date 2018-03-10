import os
import shutil

from django.db import models
from .models_user import User
from .models_tag import Tag


class Post(models.Model):
    content = models.TextField()
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(User, related_name='liked_posts')
    disliked_users = models.ManyToManyField(User, related_name='disliked_posts')

    @property
    def like_count(self):
        return len(self.liked_users.all())

    @property
    def dislike_count(self):
        return len(self.disliked_users.all())


    def liked_by(self, user):
        self.liked_users.add(user)
        self.save()

class Question(Post):
    title = models.CharField(max_length=1028)
    tags = models.ManyToManyField(Tag, related_name='tagged_questions')

    @property
    def tags_list(self):
        return ', '.join([tag.name for tag in self.tags.all()])


class Answer(Post):
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Comment(Post):
    comment_type = models.IntegerField() # 1=Question, 2=Answer, 3=Comment
    target_id = models.IntegerField()


class InvitationToAnswer(models.Model):
    inviting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitation_sent')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitation_received')
    target_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_declined = models.BooleanField(default=False)

    class Meta:
        unique_together = ('inviting_user', 'invited_user', 'target_question')
