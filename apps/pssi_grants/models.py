from django.db import models
from django.contrib.auth import get_user_model


class TravelAidStatus(models.Model):
	"""
	Travel Aid Status
	"""
	name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class TravelAid(models.Model):
    """
	Travel Aid requests
	"""
	user = models.ForeignKey(get_user_model())
	attending_conf_details = models.TextField()
	attending_conf_date = models.DateTimeField()
	talk_url = models.TextField()
	amount = models.FloatField()
	support_from_other = models.TextField()
	previous_talk_info = models.TextField(blank = True, null = True)
	availed_support_before = models.Boolean()
	availed_info = models.TextField(blank = True, null = True)
	status = models.ForeignKey(TravelAidStatus)
	comments = models.TextField(blank=True, null=True)


	 def __unicode__(self):
        return "%s %s" %(self.id, self.user)

	class Meta:
		db_table = 'travel_aid'


class WorkshopExpenses(models.Model)
	"""
	workshop WorkshopExpenses
	"""
	user = models.ForeignKey(get_user_model())
	oragnisation = models.CharField(max_length=200)
	no_of_attendees = models.IntegerField(max_length=4)
	tutor = models.TextField()
	conducted_date = models.DateTimeField()
	amount = models.IntegerField()

	class Meta:
		db_table = 'workshop_expenses'