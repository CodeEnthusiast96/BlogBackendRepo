from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .Serializers import UserSignupSerializer

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def User_signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)

        # Check if the username, email, and password are provided
        if not request.data.get('username'):
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('email'):
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('password'):
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username and email are unique
        username = request.data.get('username')
        email = request.data.get('email')     

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User successfully registered.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  




@csrf_exempt
def User_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            # Get or create a Token for the user
            token, created = Token.objects.get_or_create(user=user)

            return JsonResponse({'token': token.key,
                                'user_id': user.id,
                                'email': user.email,})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=400)