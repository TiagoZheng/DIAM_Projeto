from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

import datetime

User = get_user_model()


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    post_content = models.TextField()
    post_time = models.DateTimeField('post date')
    post_title = models.CharField(max_length=100, default='No title')
    liked_by = models.ManyToManyField(User, related_name='post_likes')
    likes_count = models.PositiveIntegerField(default=0)
    topic = models.CharField(max_length=100, null=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_posts')

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


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.post.post_title}"




class Group(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='group_members',blank=True)
    group_name = models.CharField(max_length = 50)


class GroupPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
