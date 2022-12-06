from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import gettext_lazy as _


# Name, box for details, date completed, pull in tasks by date
class TodoNote(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)
    #Store user id to keep todo lists one-to-one with users
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #split tasks by how often they must be done
    class TIME_CATEGORY(models.TextChoices):
        
        daily = 'd',_('Daily')
        weekly = 'w',_('Weekly')
        monthly = 'm',_('Monthly')
        quarterly = 'q',_('Quarterly')
        yearly = 'y',_('Yearly')

    category = models.CharField(max_length=20,default=TIME_CATEGORY.daily,choices=TIME_CATEGORY.choices)

    def __str__(self):
        return self.title