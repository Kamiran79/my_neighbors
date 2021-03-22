from rest_framework import serializers
from my_neighbors_api.models import MyNeighborsUser
from django.contrib.auth import get_user_model


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyNeighborsUser
        user = get_user_model()
        posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        fields = ('id', 'user', 'isChef', 'profile_image_url',
                  'created_on', 'menus')
        depth = 3
