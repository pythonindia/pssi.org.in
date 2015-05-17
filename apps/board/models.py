from django.db import models
from django.conf import settings
from common.models import BaseModel


class Designation(BaseModel):
    """
    Possible board positions.
    Can be added or deleted according to board decision.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BoardMember(BaseModel):
    """
    The members profile. Each have a start date and end date
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    designation = models.ForeignKey(Designation)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'designation', 'start_date', 'end_date')

    def __str__(self):
        return "{designation}: {user_name} {end_date}".format(
            designation=self.designation,
            user_name=self.user.get_full_name(),
            end_date=self.end_date
        )
