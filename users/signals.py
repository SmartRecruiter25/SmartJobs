from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name,
        )

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass  