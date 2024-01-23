from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin 
from api.model.PositionModel import Position

class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=40,unique=True)
    surname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    dni = models.CharField(max_length=10,unique=True)
    cellphone = models.CharField(max_length=15)
    birthday = models.DateField()
    image = models.CharField(max_length=150)
    date_start = models.DateField()
    date_end = models.DateField()

    position = models.ForeignKey(Position,on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname','email','dni','position']

    def __str__(self):
        return self.name