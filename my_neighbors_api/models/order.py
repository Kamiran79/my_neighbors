from django.db import models
from django.db.models.fields import TimeField
from django.utils import timezone
from django.conf import settings
from django.db.models.deletion import CASCADE, SET_NULL

class Order(models.Model):
  menu_order = models.ForeignKey("Menu",
    on_delete=SET_NULL,
    related_name="orders",
    related_query_name="order",
    null=True,
    blank=True
  )
  user_order = models.ForeignKey("MyNeighborsUser",
    on_delete=SET_NULL,
    related_name="orders",
    related_query_name="order",
    null=True,
    blank=True
  )
  reserved_date = models.DateTimeField()
  how_many = models.IntegerField()
  # this will be when the food is ready for your order.
  delivery_date = models.TimeField(blank=True)
  isConfirmed = models.BooleanField(blank=True) # Chef confirm that making the order - transaction the fee to the owner bank
  total_cost = models.FloatField()
  status = models.CharField(max_length=20) #Cooking , Ready for Pickup, Complete
  order_type = models.CharField(max_length=15) #Pickup, Delivery, Dine In
  isDelivered_user = models.BooleanField(blank=True) #user confirm picked the order make the status complete
  # The notes below for the is_delivered chef
  # chef confirm the order picked by user.
  # change the status to "user need to confirm the order received".
  # make the transction to the owner app bank. and give 
  isDelivered_chef = models.BooleanField(blank=True) 
  note = models.CharField(max_length=200, blank=True)
  report_note = models.CharField(max_length=1000, blank=True) # reports issues if there any.
