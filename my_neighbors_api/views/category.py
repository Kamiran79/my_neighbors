from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from my_neighbors_api.models import Category

class CategoriesViewSet(ViewSet):
  """My Neighbors App Category"""

  def retrieve(self, request, pk=None):
    """Handle Get request for single category

    returns:
      Response -- JSON serialized category
    """
    try:
      category = Category.objects.get(pk=pk)
      serializer = CategoryMenusSerializer(category, context={'request': request})
      return Response(serializer.data)
    except Exception as ex:
      return HttpResponseServerError(ex)

  def list(self, request):
    """Handle GET requests to get all categories
    Returns:
      Response -- JSON serialized list of categories
    """

    categories = Category.objects.all().order_by('label')

    # http://localhost:8000/categories

    # Note the addtional `many=True` argument to the
    # serializer. It's needed when you are serializing
    # a list of objects instead of a single object. 
    serializer = CategorySerializer(
      categories, many=True, context={'request': request})
    return Response(serializer.data)


  def create(self, request):
      """Handle POST operations
      Returns:
          response -- JSON serialized category instance
      """

      category = Category()
      category.label = request.data["label"]

      try:
        category.save()
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)
      
      except ValidationError as ex:
        return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


  def update(self, request, pk=None):
      """Handle PUT requests for a caregory
      Returns:
          Response -- Empty body with 204 status code
      """
      category = Category.objects.get(pk=pk)
      category.label = request.data["label"]
  
      category.save()

      return Response({}, status=status.HTTP_204_NO_CONTENT)

  def destroy(self, request, pk=None):
      """Handle DELETE requests for a single category
      Returns:
          Response -- 200, 404, or 500 status code
      """
      try:
          category = Category.objects.get(pk=pk)
          category.delete()

          return Response({}, status=status.HTTP_204_NO_CONTENT)

      except Category.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

      except Exception as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategorySerializer(serializers.HyperlinkedModelSerializer):
  """JSON Serializer for categories
  Arguments:
    serializers
  """
  class Meta:
    model = Category
    fields = ('id', 'url', 'label')

class CategoryMenusSerializer(serializers.ModelSerializer):
  """JSON Serializer for categories
  Arguments:
    serializers
  """
  class Meta:
    model = Category
    fields = ('id', 'url', 'label', 'menus')
    depth = 1
