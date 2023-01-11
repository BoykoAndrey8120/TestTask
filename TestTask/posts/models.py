from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)

    # post = Post()

    def __str__(self):
        return self.user.username


class Posts(models.Model):
    # id_post = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to='images/', default=None)
    content = models.TextField(blank=True)
    # comments = models.ForeignKey('Comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# class Posts(models.Model):
#     title = models.CharField(max_length=100)
#     # image = models.ImageField(upload_to='images', default=None)
#     content = models.TextField(blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def str(self):
#         return self.title


class Comments(models.Model):
    post = models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
        return self.content
