from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from my_neighbors_api.models import Menu, Ingredient

class MenuIngredientViewSet(ViewSet):

    def create(self, request):
        menu = Menu.objects.get(pk=request.data["menu_id"])
        ingredientlist = request.data["ingredients"]

        for ingredientId in ingredientlist:
          singleIngredient = Ingredient.objects.get(pk=ingredientId)
          menu.ingredients.add(singleIngredient)          
        
        return Response({"message": "ingredients added to menu"}, status=status.HTTP_200_OK)
