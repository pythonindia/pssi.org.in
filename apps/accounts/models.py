from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.utils import DatabaseError
from common.models import BaseModel


# class UserProfile(BaseModel):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name="profile"
#     )
#     is_pssi_member = models.BooleanField(default=False)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile(sender, **kwargs):
#     if kwargs['created'] is True:
#         try:
#             UserProfile.objects.create(user_id=kwargs['instance'].id)
#         except DatabaseError:
#             pass
