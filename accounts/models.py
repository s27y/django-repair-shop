from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from repairs.models import Job

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return ('%s %s') % (self.user.username, self.user.email)
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

