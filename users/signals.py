from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get("raw", False):
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not kwargs.get("raw", False):
        instance.userprofile.save()
