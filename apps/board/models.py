from django.db import models
from django.contrib.auth import get_user_model


class Designation(models.Model):
    """
    Posibile board positions.
    Can be added or deleted according to board decision.
    """
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class MemberProfile(models.Model):
    """
    The members profile. Each have a start date and end date
    """
    user = models.ForeignKey(get_user_model())
    designation = models.ForeignKey('Designation')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(black=True, null=True)
    designation = models.ForeignKey('Designation')
    location = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100, blank=True, Null=True)

    def __unicode__(self):
        return "{designation}: {user_name}".format(
            designation=self.designation,
            user_name=self.user.get_full_name()
        )


'''
# To be Used on Future
class Election(models.Model):
    """
    Election for board member positions
    """
    designation = models.ForeignKey('Designation')
    candidates = models.ManyToManyField(get_user_model(),
        related_name='elections_nominated')
    winner = models.ForeignKey(get_user_model(), black=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(black=True, null=True)

    def __unicode__(self):
        return '{designation}: {date}'.format(
            designation=self.designation,
            date=self.start_date
        )


class Vote(models.Model):
    """
    The vote entries. These should not be visible in the admin panel.
    """
    election = models.ForeignKey('Election')
    user = models.ForeignKey(get_user_model())
    candidate = models.ForeignKey(get_user_model())
    created_at = models.DateTimeField(auto_now_add=True)

'''