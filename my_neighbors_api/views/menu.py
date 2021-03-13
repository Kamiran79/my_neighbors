"""View module for handling requests about game types"""
from my_neighbors_api.models.ingredient import Ingredient
from my_neighbors_api.models.category import Category
from django.db.models.base import Model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from my_neighbors_api.models import Menu

class MenuView(ViewSet):
  """My Neighbors Menus"""

  def retrieve(self, request, pk=None):
        """Handle GET requests for single menu

        Returns:
            Response -- JSON serialized menu
        """
        try:
          menu = Menu.objects.get(pk=pk)
          serializer = MenuViewSerializer(menu, context={'request': request})
          return Response(serializer.data)
        except Exception as ex:
          return HttpResponseServerError(ex)
  
  def list(self, reguest):
        """Handle GET requests to get all menus

        Returns:
            Response -- JSON serialized list of menus
        """
        menus = Menu.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = MenuViewSerializer(
            menus, many=True, context={'request': reguest})
        return Response(serializer.data)

class MenuViewSerializer(serializers.ModelSerializer):
    """JSON serializer for menus

    Arguments:
        serializers
    """    
    class Meta:
        model = Menu
        fields = ('id', 'url', 'name',
        'ready_eat', 'foodImgUrl', 'delivery', 'pick_up', 'dine_in',
        'price', 'status', 'how_many_left', 'my_neighbor_user',
        'category','ingredients')
        depth = 1
