from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    like = models.BigIntegerField(default=0)
    text = models.TextField(max_length=1000, blank=True, default='')
