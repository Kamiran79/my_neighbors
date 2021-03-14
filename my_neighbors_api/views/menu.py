"""View module for handling requests about game types"""
from django.core.exceptions import ValidationError
from my_neighbors_api.models.ingredient import Ingredient
from my_neighbors_api.models.category import Category
from django.db.models.base import Model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from my_neighbors_api.models import Menu, MyNeighborsUser, Category, Ingredient

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

  def create(self, request):
        chef = MyNeighborsUser.objects.get(user=request.auth.user)

        menu = Menu()
        menu.name = request.data["name"]
        menu.ready_eat = request.data["ready_eat"]
        menu.foodImgUrl = request.data["foodImgUrl"]
        menu.delivery = request.data["delivery"]
        menu.pick_up = request.data["pick_up"]
        menu.dine_in = request.data["dine_in"]
        menu.price = request.data["price"]
        menu.status = request.data["status"]
        menu.how_many_left = request.data["how_many_left"]

        menu.my_neighbor_user = chef

        category = Category.objects.get(pk=request.data["category"])
        menu.category = category

        try:
            menu.save()
            menu.ingredients.set(request.data["ingredients"])
            menu.save()
            serializer = MenuViewSerializer(menu, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

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
