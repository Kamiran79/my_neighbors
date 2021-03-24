"""my_neighbors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from my_neighbors_api.views.auth import get_current_user
from django import urls
from django.contrib import admin
from django.db import router
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from my_neighbors_api.views import register_user, login_user
from my_neighbors_api.views import MenuView, CategoriesViewSet, IngredientsViewSet, MenuRatingViewSet, UsersViewSet
from my_neighbors_api.views import get_current_user, is_current_user_admin, get_current_user_zipcode
from my_neighbors_api.views import MenuIngredientViewSet
from my_neighbors_api.views import *
from my_neighbors_api.models import *


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'menus', MenuView, 'menu')
router.register(r'categories', CategoriesViewSet, 'category')
router.register(r'ingredients', IngredientsViewSet, 'ingredient')
router.register(r'menuratings', MenuRatingViewSet, 'menurating')
router.register(r'users', UsersViewSet, 'users')
router.register(r'menuingredients', MenuIngredientViewSet, 'menuingredients')
router.register(r'orders', Orders, 'order')

urlpatterns = [
    path('', include(router.urls)),
    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('get_current_user', get_current_user),
    path('is_admin', is_current_user_admin),    
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
