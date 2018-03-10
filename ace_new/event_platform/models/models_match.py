import os
import shutil

from django.db import models
from .models_user import User

class MatchRequest(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_request_sent')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_request_received')
    is_declined = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('mentee', 'mentor')
