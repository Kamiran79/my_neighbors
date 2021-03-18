"""View module for handling requests about tags"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from my_neighbors_api.models import Ingredient

class IngredientsViewSet(ViewSet):
  """ Ingredients"""

  def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized tag instance
        """

        ingredient = Ingredient()
        ingredient.label = request.data["label"]

        try:
          ingredient.save()
          serializer = IngredientSerializer(ingredient, context={'request': request})
          return Response(serializer.data)
        except ValidationError as ex:
          return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
        """Handle DELETE requests for a single ingredient
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredient.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Ingredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def retrieve(self, request, pk=None):
      """Handle GET requests for single ingredient
      Returns:
          Response -- JSON serialized tag instance
      """
      try:
          ingredient = Ingredient.objects.get(pk=pk)
          serializer = IngredientSerializer(ingredient, context={'request': request})
          return Response(serializer.data)
      except Exception as ex:
          return HttpResponseServerError(ex)


  def list(self, request):
      """Handle GET requests to ingredients resource
      Returns:
          Response -- JSON serialized list of ingrediants
      """
      ingrediants = Ingredient.objects.all()

      serializer = IngredientSerializer(
          ingrediants, many=True, context={'request': request})
      return Response(serializer.data)

  def update(self, request, pk=None):
      """Handle PUT requests for a ingrediant
      Returns:
          Response -- Empty body with 204 status code
      """
      ingredient = Ingredient.objects.get(pk=pk)
      ingredient.label = request.data["label"]
  
      ingredient.save()

      return Response({}, status=status.HTTP_204_NO_CONTENT)


class IngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for ingrediants
    Arguments:
        serializer type
    """

    class Meta:
        model = Ingredient
        url = serializers.HyperlinkedIdentityField(
            view_name='ingredient',
            lookup_field='id'
        )
        fields = ('id', 'url', 'label')
