from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
@receiver(post_save, sender=CustomUser, dispatch_uid='save_new_user_profile')
def create_profile(sender, instance, created, **kwargs):
    print("yes")
    user = instance
    if created:
        profile = Profile.objects.create(owner=user)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    print("done")
    instance.profile.save()

@receiver(post_save, sender=CustomUser, dispatch_uid='grouping_admins')
def grouping_admin(sender, instance, created, **kwargs):
    if instance.is_superuser:
        employer = Group.objects.get(name='Employer')
        instance.groups.add(employer)
