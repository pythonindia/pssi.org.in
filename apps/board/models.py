from django.db import models
from django.conf import settings
from common.models import BaseModel


class Designation(BaseModel):
    """
    Posibile board positions.
    Can be added or deleted according to board decision.
    """
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class BoardMember(BaseModel):
    """
    The board members. Each have a start date and end date
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    designation = models.ForeignKey('Designation')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'designation', 'start_date', 'end_date')

    def __unicode__(self):
        return "{designation}: {user_name}".format(
            designation=self.designation,
            user_name=self.user.get_full_name()
        )


# class Election(BaseModel):
#     """
#     Election for board member positions
#     """
#     designation = models.ForeignKey('Designation')
#     candidates = models.ManyToManyField(settings.AUTH_USER_MODEL,
#         related_name='elections_nominated')
#     winner = models.ForeignKey(settings.AUTH_USER_MODEL, black=True, null=True)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(black=True, null=True)

#     def __unicode__(self):
#         return '{designation}: {date}'.format(
#             designation=self.designation,
#             date=self.start_date
#         )


# class Vote(BaseModel):
#     """
#     The vote entries. These should not be visible in the admin panel.
#     """
#     election = models.ForeignKey('Election')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     candidate = models.ForeignKey(settings.AUTH_USER_MODEL)
#     created_at = models.DateTimeField(auto_now_add=True)

