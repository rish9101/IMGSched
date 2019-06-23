from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField( _('email address'), unique=True, primary_key=True)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

   
#class Users(models.Model):
#    name = models.CharField(max_length=100)
#    email = models.EmailField(max_length=254, unique=True, primary_key=True)
#    admin = models.IntegerField(default=0)
#    def __str__(self):
#        return self.email
    #meeting_scheduled = models.ForeignKey(MeetingsTable, related_name='scheduled', on_delete=models.CASCADE)

class MeetingsTable(models.Model):
    meeting_date_time = models.DateTimeField(auto_now=False,auto_now_add=False)
    purpose = models.TextField(blank=True)
    scheduler_id = models.ForeignKey(User, related_name='meetings_scheduled', on_delete=models.CASCADE)
    people_invited = models.ManyToManyField(User, blank=False)

class CommentsTable(models.Model):
    commentor_email = models.ForeignKey(User, related_name='commentor',on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    meeting = models.ForeignKey(MeetingsTable, related_name='commented_on', on_delete=models.CASCADE)
    meeting_date_time = models.DateTimeField(auto_now=False,auto_now_add=False)
