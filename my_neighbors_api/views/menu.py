"""View module for handling requests about game types"""
import os
import base64
from django.utils import timezone
from django.core.exceptions import ValidationError
from my_neighbors_api.models.ingredient import Ingredient
from my_neighbors_api.models.category import Category
from django.db.models.base import Model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from my_neighbors_api.models import Menu, MyNeighborsUser, Category, Ingredient, my_neighbors_user
from my_neighbors_api.serializer import MenuSerializer, MenuViewSerializer

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

        #Chef get menu list
        user_id = self.request.query_params.get('user_id', None)

        user = self.request.query_params.get('user', None)

        # These filters all you to do http://localhost:8000/posts?category=1 or
        # http://localhost:8000/menus?user=1 or
        # http://localhost:8000/posts?category=1&user=2

        #http://localhost:8000/menus?zipCode=37122
        #This is to get menu list for a user
        zipCode = self.request.query_params.get('zipCode', None)
        if zipCode is not None:
            menus = menus.filter(my_neighbor_user__zipCode = zipCode)
            menus = menus.filter(status = True)
        #http://localhost:8000/menus?user_id=4
        if user_id is not None:
            menus = menus.filter(my_neighbor_user__user = user_id)

        if user is not None:
            menus = menus.filter(my_neighbors_user__id=user)
        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = MenuViewSerializer(
            menus, many=True, context={'request': reguest})
        return Response(serializer.data)

  def create(self, request):
        chef = MyNeighborsUser.objects.get(user=request.auth.user)

        new_menu = Menu()
        new_menu.name = request.data["name"]
        # Format post image
        # format, imgstr = request.data['foodImgUrl'].split(';base64,')
        # ext = format.split('/')[-1]
        # image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')        

        if "foodImgUrl" in request.data:
            format, imgstr = request.data["foodImgUrl"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{new_menu.id}-{request.data["name"]}.{ext}')

            new_menu.foodImgUrl = data


        
        
        #menu.ready_eat = request.data["ready_eat"]
        new_menu.ready_eat = timezone.now()
        #menu.foodImgUrl = request.data["foodImgUrl"]        
        #new_menu.foodImgUrl = image_data
        # menu.delivery = request.data["delivery"]
        # menu.pick_up = request.data["pick_up"]
        # menu.dine_in = request.data["dine_in"]
        new_menu.delivery = True
        new_menu.pick_up = False
        new_menu.dine_in = True
        new_menu.price = request.data["price"]
        new_menu.status = True
        new_menu.how_many_left = request.data["how_many_left"]
        new_menu.content = request.data["content"]

        new_menu.my_neighbor_user = chef

        category = Category.objects.get(pk=request.data["category"])
        new_menu.category = category

        try:
            new_menu.save()
            new_menu.ingredients.set(request.data["ingredients"])
            new_menu.save()
            serializer = MenuViewSerializer(new_menu, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
      chef = MyNeighborsUser.objects.get(user=request.auth.user)

      image_data = ''

      # Check for an image update
      menu = Menu.objects.get(pk=pk)
      menu_image = Menu.objects.get(pk=pk).foodImgUrl.name
      image_path = request.data['foodImgUrl'].split('media/')
      if request.data['foodImgUrl'] != "":
        if image_path[-1] == menu_image:
            image_data = image_path[1]
        # Format new post image
        elif request.data['foodImgUrl']:
            format, imgstr = request.data['foodImgUrl'].split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')      
        
        menu.foodImgUrl = image_data
      
      
      menu.name = request.data["name"]
      menu.ready_eat = request.data["ready_eat"]
      menu.content = request.data["content"]
      #menu.ready_eat = timezone.now()
      
    #   menu.delivery = request.data["delivery"]
    #   menu.pick_up = request.data["pick_up"]
    #   menu.dine_in = request.data["dine_in"]
      #menu.delivery = True
      #menu.pick_up = False
      #menu.dine_in = True
    #   menu.price = request.data["price"]
    #   menu.status = request.data["status"]
    #   menu.how_many_left = request.data["how_many_left"]

      menu.my_neighbor_user = chef

      category = Category.objects.get(pk=request.data["category"])
      menu.category = category
      menu.ingredients.set(request.data["ingredients"])
      menu.save()
      return Response({}, status=status.HTTP_204_NO_CONTENT)

  def destroy(self, request, pk=None):
      try:
          # If user is an admin (is_staff == true), then we can just
          # delete the post by pk.  Otherwise, we should verify that
          # the user owns that post before deleting it.
          if request.user.is_staff:
              menu = Menu.objects.get(pk=pk)
          else:
              menu = Menu.objects.get(pk=pk, rareuser_id=request.user.id)

          menu.delete()
          return Response({}, status=status.HTTP_204_NO_CONTENT)

      except Menu.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(methods=['POST'], detail=True)
    # def remove_tag(self, request, pk=None):

    #     try:
    #         menu = Menu.objects.get(pk=pk)
    #         ingredient = Ingredient.objects.get(pk=request.data['tag_id'])
    #         menu.ingredients.remove(ingredient)

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except Menu.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Ingredient.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def partial_update(self, request, pk=None):
    #     menu= Menu.objects.get(pk=pk)
    #     serializer = MenuSerializer(menu, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
