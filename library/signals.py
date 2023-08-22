from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NormalUser


@receiver(post_save, sender=User)
def create_or_update_normal_user(sender, instance, created, **kwargs):
    if created:
        NormalUser.objects.create(user=instance)
    else:
        instance.normaluser.save()
