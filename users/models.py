from django.db import models
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import NeighbourHood
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = ImageField(blank=True, manual_crop="")
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=60, blank=True)
    contact = models.CharField(max_length=60,blank=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True,blank=True)
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()