from api.model.UserModel import User
from django.db import models

class Notification(models.Model):
    message = models.TextField()
    user_Id = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
