from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def getfilepath(instance, filename):
	return '/'.join(['blueprints',str(instance.user.id),filename,])

class UserProfile(models.Model):
    """
    Description: User Profile
    """
    user = models.OneToOneField(User)
    organisation = models.CharField(max_length=200)
    address = models.TextField()
    mobile_no = models.CharField(max_length=200)
    def __unicode__(self):
    	return self.user.first_name


class BluePrint(models.Model):
    """
    Description: Blue print upload
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    desp = models.TextField()
    blueprint = models.FileField(upload_to=getfilepath)
    def __unicode__(self):
    	return self.user.first_name