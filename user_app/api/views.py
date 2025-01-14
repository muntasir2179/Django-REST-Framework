from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import RegistrationSerializer


@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()   # deleting the token which will prevent further access
        return Response({'response': 'Logout Successful!'} ,status=status.HTTP_200_OK)


@api_view(["POST",])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()   # our overridden save() method will return the credentials of the created account
            data['response'] = 'Registration Successful!'
            data['username'] = account.username   # accessing username through account
            data['email'] = account.email   # accessing email through account
            
            token = Token.objects.get_or_create(user=account)[0].key    # if token is already exists for this user it will just return it, if not exists it will create a new one and return
            data['token'] = token
        else:
            data = serializer.errors   # if registration is failed we will return error messages from serializer
        
        return Response(data, status=status.HTTP_201_CREATED)
