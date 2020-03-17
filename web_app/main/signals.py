from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import logging
from .models import Subscription, Post

logger = logging.getLogger(__name__)


def notification(sender, instance, **kwargs):
    subscribers = Subscription.objects.filter(blogger_id=instance.author_id).values('subscriber_id')
    subscribers = {x['subscriber_id'] for x in subscribers}
    for user_id in subscribers:
        user = User.objects.get(pk=user_id)
        user_email = user.email
        if user_email:
            base_url = settings.SITE_URL
            port = settings.SITE_PORT
            post_link = instance.get_absolute_url()
            message = f"Hello, there is a new post! Link: {base_url}:{port}{post_link}"

            em = EmailMessage(subject='New post!', body=message, to=[user_email])
            try:
                em.send()
            except Exception as e:
                logger.error(e, type(e))


post_save.connect(notification, sender=Post)