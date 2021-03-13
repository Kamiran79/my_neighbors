from my_neighbors_api.models.category import Category
from my_neighbors_api.models.ingredient import Ingredient
from my_neighbors_api.models.menu import Menu
from django.contrib import admin
from my_neighbors_api.models import Menu, Ingredient, Category

# Register your models here.
admin.site.register(Menu)
admin.site.register(Ingredient)
admin.site.register(Category)
