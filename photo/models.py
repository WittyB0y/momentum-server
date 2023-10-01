import random

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class RandomPhoto:
    __one = 'https://i.yapx.ru/WiO5Ms.png'
    __two = 'https://i.yapx.ru/WiO6Gs.png'
    __three = 'https://i.yapx.ru/WiO6Zs.png'
    __four = 'https://i.yapx.ru/WiO6ns.png'
    __five = 'https://i.yapx.ru/WiO66s.png'
    __six = 'https://i.yapx.ru/WiO7Fs.png'
    all_photos = [__one, __two, __three, __four, __five, __six, ]

    @classmethod
    def get_random(cls, method):
        return method(cls.all_photos)


class UserAvatar(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=False)
    count = models.IntegerField(default=1, null=False)
    image = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    updatedPhoto = models.DateTimeField(auto_now=True)
    linkPhoto = models.URLField(null=False)


@receiver(post_save, sender=User)
def create_user_avatar(sender, instance, created, **kwargs):
    if created:
        UserAvatar.objects.create(
            userID=instance,
            linkPhoto=RandomPhoto.get_random(random.choice),
        )


@receiver(post_save, sender=User)
def save_user_avatar(sender, instance, **kwargs):
    instance.useravatar.save()
