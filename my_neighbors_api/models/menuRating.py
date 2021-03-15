from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.core.validators import MaxValueValidator, MinValueValidator
from .menu import Menu

class MenuRating(models.Model):
  rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)
  my_neighbors_user = models.ForeignKey("MyNeighborsUser",
    on_delete=models.DO_NOTHING,
  )
  menu = models.ForeignKey(Menu,
    on_delete=models.DO_NOTHING,
  )

  class Meta:
    verbose_name = ("rating_menu")
    verbose_name_plural = ("ratings_menu")
