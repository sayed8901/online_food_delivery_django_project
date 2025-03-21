# urls.py in accounts app
from django.urls import path
from .views import (
    OwnerRegisterAPIView, UserRegisterAPIView, LoginAPIView, LogoutAPIView, 
    OwnerListAPIView, UserListAPIView
)


urlpatterns = [
    path('register/owner/', OwnerRegisterAPIView.as_view(), name='owner_register'),
    path('register/user/', UserRegisterAPIView.as_view(), name='user_register'),
    
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),

    path('owners/', OwnerListAPIView.as_view(), name='owner_list'),
    path('users/', UserListAPIView.as_view(), name='user_list'),
]

