"""
Defines models
"""
from django.db import models


class User(models.Model):
    """
    Represents single user
    """
    user_id = models.IntegerField()
    name = models.CharField(max_length=120)
    avatar = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name


class Presence(models.Model):
    """
    Presence model
    """
    user = models.ForeignKey('analyzer.User', verbose_name='User')
    day = models.DateField('Data')
    start = models.TimeField('Start')
    end = models.TimeField('End')
