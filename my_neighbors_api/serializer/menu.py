from rest_framework import serializers
from my_neighbors_api.models import Menu, my_neighbors_user


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        my_neighbors_user = serializers.PrimaryKeyRelatedField(
            many=False, read_only=True)
        category = serializers.PrimaryKeyRelatedField(
            many=False, read_only=True)
        fields = ('id', 'my_neighbors_user', 'category', 'title',
                  'ready_eat', 'foodImgUrl', 'status', 'ingredients','content')
        depth = 2

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
        'category','ingredients','content')
        depth = 3        
