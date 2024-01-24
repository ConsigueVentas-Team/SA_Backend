from django.urls import path, include
from api import views

urlpatterns = [
    #--------- AUTHENTICATIONS URLs ---------#
    path('register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario
    path('login',views.UserLoginView.as_view(),name="user_login"),#login
    
    path('profile',views.UserProfileView.as_view(),name="user_user"),#Datos del usuario authenticado
]