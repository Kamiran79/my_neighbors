from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class MyNeighborsUser(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
  isChef = models.BooleanField(default=False)
  address = models.CharField(max_length=50)
  city = models.CharField(max_length=25)
  state = models.CharField(max_length=2)
  zipCode = models.CharField(max_length=5)
  profile_imgage_url = models.ImageField(blank=True)
