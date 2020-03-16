from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=250, db_index=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title


class Subscription(models.Model):
    subscriber_id = models.IntegerField(db_index=True)
    blogger_id = models.IntegerField(db_index=True)