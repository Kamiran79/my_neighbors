"""View module for handling requests about customer order"""
import datetime
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from my_neighbors_api.models import Order, MyNeighborsUser, Menu
from .menu import MenuViewSerializer


class OrderLineItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for line items """

    menu = MenuViewSerializer(many=False)

    class Meta:
        model = Menu
        url = serializers.HyperlinkedIdentityField(
            view_name='get_menu',
            lookup_field='id'
        )
        fields = ('id', 'menu')
        depth = 1

class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for customer orders"""

    # get_menu = OrderLineItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'url', 'reserved_date', 'note', 'user_order', 'menu_order', 'chef_order'
        , 'delivery_date', 'total_cost', 'status', 'order_type' )
        depth = 1


class Orders(ViewSet):
    """View for interacting with customer orders"""

    def retrieve(self, request, pk=None):
        """
        @api {GET} /cart/:id GET single order
        @apiName GetOrder
        @apiGroup Orders
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiSuccess (200) {id} id Order id
        @apiSuccess (200) {String} url Order URI
        @apiSuccess (200) {String} created_date Date order was created
        @apiSuccess (200) {String} payment_type Payment URI
        @apiSuccess (200) {String} customer Customer URI
        @apiSuccessExample {json} Success
            {
                "id": 1,
                "url": "http://localhost:8000/orders/1",
                "created_date": "2019-08-16",
                "payment_type": "http://localhost:8000/paymenttypes/1",
                "customer": "http://localhost:8000/customers/5"
            }
        """
        try:
            user_order = MyNeighborsUser.objects.get(user=request.auth.user)
            order = Order.objects.get(pk=pk, user_order=user_order)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)

        except Order.DoesNotExist as ex:
            return Response(
                {'message': 'The requested order does not exist, or you do not have permission to access it.'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /order/:id PUT new payment for order
        @apiName AddPayment
        @apiGroup Orders
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id Order Id route parameter
        @apiParam {id} payment_type Payment Id to pay for the order
        @apiParamExample {json} Input
            {
                "payment_type": 6
            }
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.get(pk=pk, customer=customer)
        order.payment_type = request.data["payment_type"]
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """
        @api {GET} /orders GET customer orders
        @apiName GetOrders
        @apiGroup Orders
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} payment_id Query param to filter by payment used
        @apiSuccess (200) {Object[]} orders Array of order objects
        @apiSuccess (200) {id} orders.id Order id
        @apiSuccess (200) {String} orders.url Order URI
        @apiSuccess (200) {String} orders.created_date Date order was created
        @apiSuccess (200) {String} orders.payment_type Payment URI
        @apiSuccess (200) {String} orders.customer Customer URI
        @apiSuccessExample {json} Success
            [
                {
                    "id": 1,
                    "url": "http://localhost:8000/orders/1",
                    "created_date": "2019-08-16",
                    "payment_type": "http://localhost:8000/paymenttypes/1",
                    "customer": "http://localhost:8000/customers/5"
                }
            ]
        """
        #http://localhost:8000/orders?chef_order=13 chef can get all his orders
        chef_order = self.request.query_params.get('chef_order', None)
        if chef_order is not None:
            orders = Order.objects.filter(chef_order__user=chef_order)
        else:
            #http://localhost:8000/orders user can get all his orders
            user_order = MyNeighborsUser.objects.get(user=request.auth.user)
            orders = Order.objects.filter(user_order=user_order)

        menu = self.request.query_params.get('menu_id', None)
        if menu is not None:
            orders = orders.filter(menu__id=menu)

        json_orders = OrderSerializer(
            orders, many=True, context={'request': request})

        return Response(json_orders.data)

    def create(self, request):
      user_order = MyNeighborsUser.objects.get(user=request.auth.user)

      order = Order()
      order.reserved_date = request.data["reserved_date"]
      order.how_many = request.data["how_many"]
      order.note = request.data["note"]
      order.user_order = user_order
      menu_order = Menu.objects.get(pk=request.data["menu_order"])
      #print(menu_order.my_neighbor_user.auth.user)

      #chef_order = MyNeighborsUser.objects.get(pk=menu_order.my_neighbor_user)
      chef_order = menu_order.my_neighbor_user
      order.chef_order = chef_order
      #print(chef_user_id)
      order.menu_order = menu_order
      order.delivery_date = request.data["delivery_date"]
      order.total_cost = request.data["total_cost"]
      order.status = request.data["status"]
      order.order_type = request.data["order_type"]
      order.isConfirmed = False
      order.isDelivered_chef = False
      order.isDelivered_user = False

      try:
        order.save()
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

      except ValidationError as ex:
          return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
