import os
import shutil

from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    tag_type = models.IntegerField() # 0=No type, 1=Living, 2=Study, 3=Career

    @property
    def tag_type_str(self):
        return 'Living' if self.tag_type == 1 else 'Study' if self.tag_type == 2 else 'Career' if self.tag_type == 3 else 'No Type'
