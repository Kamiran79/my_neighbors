import json
from django.http import HttpResponse, request
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from my_neighbors_api.models import MyNeighborsUser

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # check if user exists in db
    user_exists = User.objects.filter(email=req_body['email']).exists()

    if user_exists:
        data = json.dumps({"msg": "user already exists"})
        return HttpResponse(data, content_type='application/json')


    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        is_active=True,
        is_staff=req_body['isChef']
    )

    # Now save the extra info in the levelupapi_gamer table
    myNeighborsUser = MyNeighborsUser.objects.create(
        isChef=req_body['isChef'],
        address=req_body['address'],
        city=req_body['city'],
        state=req_body['state'],
        zipCode=req_body['zipCode'],
        telephone=req_body['telephone'],
        user=new_user
    )

    # Commit the user to the database by saving it
    myNeighborsUser.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')      

@csrf_exempt
def is_current_user_admin(request):

    req_body = json.loads(request.body.decode())

    try:
        user_id = Token.objects.get(key=req_body['token']).user_id
        is_admin = User.objects.get(pk=user_id).is_staff
        data = json.dumps({"is_user_admin": is_admin})
        return HttpResponse(data, content_type="application/json")
    except Token.DoesNotExist:
        data = json.dumps(
            {"valid": False, "msg": "No currently authenticated user."}
        )
        return HttpResponse(data, content_type="application/json")

@csrf_exempt
def get_current_user(request):

    req_body = json.loads(request.body.decode())

    try:
        user_id = Token.objects.get(key=req_body['token']).user_id
        data = json.dumps({"user_id": user_id})
        return HttpResponse(data, content_type="application/json")
    except Token.DoesNotExist:
        data = json.dumps(
            {"valid": False, "msg": "No currently authenticated user."})
        return HttpResponse(data, content_type='application/json')
