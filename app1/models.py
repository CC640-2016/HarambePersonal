from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Task(models.Model):
    description = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    
    def __str__(self):
        return self.description