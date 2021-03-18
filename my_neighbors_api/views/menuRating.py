from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from my_neighbors_api.models import MenuRating
from my_neighbors_api.serializer import MenuRatingSerializer

class MenuRatingViewSet(ViewSet):
  def retrieve(self, request, pk=None):
    try:
      menuRating = MenuRating.objects.get(pk=pk)
      serializer = MenuRatingSerializer(menuRating, context={'request': request})
      return Response(serializer.data)
    except Exception as ex:
      return HttpResponseServerError(ex)
