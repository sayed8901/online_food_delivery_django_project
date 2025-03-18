# serializers.py in accounts app
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.hashers import make_password

User = get_user_model()


# Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'role']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove confirm_password
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)



# login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, max_length=20)


# logout serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)



# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', 'first_name', 'last_name', 'email', 'role']

