from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin 
from api.model.PositionModel import Position
from api.enums import RoleEnum
import os

def avatar_path(instance, filename):
    # Obtén el nombre de usuario del objeto de usuario
    dni = instance.dni
    # Obtén la extensión del archivo
    _, ext = os.path.splitext(filename)
    # Construye el nombre del archivo de avatar usando el nombre de usuario y la extensión
    return os.path.join('photos', f'{dni}{ext}')

class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=40,unique=True)
    surname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    status_description = models.CharField(max_length=100,null=True, blank=True)
    dni = models.CharField(max_length=10,unique=True)
    cellphone = models.CharField(max_length=15)
    birthday = models.DateField()
    avatar = models.ImageField(upload_to=avatar_path)
    date_start = models.DateField()
    date_end = models.DateField()
    shift = models.CharField(max_length=15)

    position = models.ForeignKey(Position,on_delete=models.CASCADE)
    role = models.IntegerField(choices=[(e.value, e.name) for e in RoleEnum])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname','email','dni','position','password']

    def __str__(self):
        return self.name