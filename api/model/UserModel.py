from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin 

class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40,unique=True)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    dni = models.CharField(max_length=9)
    cellphone = models.CharField(max_length=30)
    birthday = models.DateField()
    # url_image = models.CharField(max_length=4000)
    # position_id = models.ForeignKey

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)#Fecha de creacion
    updated_at = models.DateTimeField(auto_now=True)#Fecha de actualización
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname','email']

    def __str__(self):
        return self.name