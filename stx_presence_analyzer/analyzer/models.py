from django.db import models

class User(models.Model):
    """
    User model
    """
    name = models.CharField(max_length=20)
    avatar = models.CharField(max_length=120)
    user_id = models.IntegerField(max_length=20)


class PresenceStartEnd(models.Model):
    """
    Presence by start and end model
    """
    user = models.ForeignKey('User')
    day = models.DateField('Day')
    start = models.TimeField('Start')
    end = models.TimeField('End')


class PresenceByWeekday(models.Model):
	"""
	Presence weekday model
	"""
	user = models.ForeignKey('User')
	day = models.DateField('Day')
	presence_sum = models.TimeField('Sum')

        
class PresenceMeanTime(models.Model):
	"""
	Mean time presence model
	"""
	user = models.ForeignKey('User')
	day = models.DateField('Day')
	mean_presence = models.TimeField('Mean')