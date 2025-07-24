from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
# Models for Category
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name

# Models for Event
class Event(models.Model):
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('COMPLETED', 'Completed'),
    ]
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPCOMING')
    # participants = models.ManyToManyField(User, related_name='participated_events', blank=True)
    rsvped_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvp_events', blank=True)
    event_image = models.ImageField(upload_to="Event_Image",blank=True,null=True)

    def __str__(self):
        return f"{self.name} ({self.date})"
    
# models for Participent
# this will replace by user 
# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     events = models.ManyToManyField(Event)

#     def __str__(self):
#         return self.name 

