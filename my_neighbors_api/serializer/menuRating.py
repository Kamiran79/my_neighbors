
from rest_framework import serializers
from my_neighbors_api.models import MenuRating, MyNeighborsUser, Menu, my_neighbors_user

class MenuRatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = MenuRating
    fields = ('id', 'url', 'rating', 'my_neighbors_user', 'menu')
    depth = 1

# class MenuRatingSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for menu rating
#     Arguments:
#         serializers
#     """
#     my_neighbors_user = RatingCustomerSerializer(many=False)
#     menu = ProductRatingSerializer(many=False)

#     class Meta: 
#         model = MenuRating
#         url = serializers.HyperlinkedIdentityField(
#             view_name="menurating",
#             lookup_field= 'id'
#         )
#         fields = ('id', 'rating', 'my_neighbors_user', 'menu')

# class MenuRateSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON Serializer for Menu"""
#     class Meta: 
#         model= Menu
#         url = serializers.HyperlinkedIdentityField(
#             view_name= 'menu',
#             lookup_field= 'id'
#         )
#         fields = ('id', 'name')

# class UserMenuRateSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for user menuratings"""
#     user = UserSerializer(many=False)
    
#     class Meta:
#         model = Customer
#         url = serializers.HyperlinkedIdentityField(
#             view_name='customer',
#             lookup_field='id'
#         )
#         fields = ('id', 'user')
#         depth = 1

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON Serializer for user"""
#     class Meta:
#         model= User
#         url = serializers.HyperlinkedIdentityField(
#             view_name= 'user',
#             lookup_field= 'id'
#         )
#         fields = ('id', 'first_name', 'last_name')
