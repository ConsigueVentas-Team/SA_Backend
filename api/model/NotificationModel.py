from api.model.UserModel import User
from django.db import models

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
