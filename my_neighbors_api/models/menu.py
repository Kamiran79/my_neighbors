#import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.deletion import CASCADE, SET_NULL

class Menu(models.Model):

  #def upload_to(instance, filename):
  #  return f"menus/{instance.my_neighbors_user.id}-{uuid.uuid4()}"

  name = models.CharField(max_length=50)
  ready_eat = models.DateTimeField()
  foodImgUrl = models.ImageField(blank=True)
  delivery = models.BooleanField()
  pick_up = models.BooleanField()
  dine_in = models.BooleanField()
  price = models.FloatField()
  status = models.BooleanField()
  how_many_left = models.IntegerField()
  my_neighbor_user = models.ForeignKey("MyNeighborsUser",
    on_delete=CASCADE,
    related_name="menus",
    related_query_name="menu"
  )
  category = models.ForeignKey("Category",
    on_delete=SET_NULL,
    # did not CASCADE here, so menu stays even after category is deleted
    related_name="menus",
    related_query_name="menu",
    null=True,
    # added above if the category was deleted
    blank=True
  )
