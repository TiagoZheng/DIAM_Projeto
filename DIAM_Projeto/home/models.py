from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from six import string_types
import datetime


# Create your models here.
class Post(models.Model):
    post_content = models.CharField(max_length=300)
    post_time = models.DateTimeField('post date')
    likes = models.ManyToManyField(User, related_name='post_likes')

    def __str__(self):
        return self.post_content

    def is_recent_publish(self):
        return self.post_time >= timezone.now() - datetime.timedelta(days=1)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    post_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
