from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.core.validators import MaxValueValidator, MinValueValidator
from .my_neighbors_user import MyNeighborsUser


class ChefRating(models.Model):
  rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)
  my_user_user = models.ForeignKey("MyNeighborsUser",
    on_delete=models.DO_NOTHING,
    related_name="chefRatings_user",
    related_query_name="chefRating_user",
  )
  my_user_chef = models.ForeignKey("MyNeighborsUser",
    on_delete=models.DO_NOTHING,
    related_name="chefRatings_chef",
    related_query_name="chefRating_chef",
  )
  class Meta:
    verbose_name = ("rating_chef")
    verbose_name_plural = ("ratings_chef")    
