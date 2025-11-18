from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ninja import P
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating profile for user: {instance.username}")
        print(sender)
        Profile.objects.create(user=instance)
    else:
        print(f"Updating failed profile for user: {instance.username}")


@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    print(f"Saving profile for user: {instance.user.username}")
    # instance.save()
    print(sender)
    print(instance)
    print(kwargs)
    instance.user.save()