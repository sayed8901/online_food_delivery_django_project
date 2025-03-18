# views.py in accounts app
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwner, IsUser
from django.contrib.auth import authenticate

from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UserSerializer


User = get_user_model()




# Register API
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# creating views for login functionality
class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serialized_data = self.serializer_class(data = request.data)

        if serialized_data.is_valid():
            username = serialized_data.validated_data['username']
            password = serialized_data.validated_data['password']
            user = authenticate(username = username, password = password)

            if user:
                refresh = RefreshToken.for_user(user)  # Generate JWT tokens
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'role': user.role
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credential'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)




# Logout API
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"error": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)





# API to get all owners
class OwnerListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        owners = User.objects.filter(role="owner")
        serializer = UserSerializer(owners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# API to get all normal users
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        normal_users = User.objects.filter(role="user")
        serializer = UserSerializer(normal_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
