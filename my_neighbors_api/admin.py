from my_neighbors_api.models.category import Category
from my_neighbors_api.models.ingredient import Ingredient
from my_neighbors_api.models.menu import Menu
from django.contrib import admin
from my_neighbors_api.models import Menu, Ingredient, Category, Order, ChefRating, MenuRating

# Register your models here.
admin.site.register(Menu)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ChefRating)
admin.site.register(MenuRating)
