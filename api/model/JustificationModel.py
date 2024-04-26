from django.db import models
from api.enums import JustificationStatus
from api.model.UserModel import User
import os

def avatar_path(instance, filename):
    # Obtén el nombre de usuario del objeto de usuario
    dni = instance.dni
    # Obtén la extensión del archivo
    _, ext = os.path.splitext(filename)
    # Construye el nombre del archivo de avatar usando el nombre de usuario y la extensión
    return os.path.join('photos', f'{dni}{ext}')
  
class Justification(models.Model):
  justification_date = models.DateField()
  reason = models.TextField()
  evidence = models.ImageField(upload_to=avatar_path)
  justification_type = models.BooleanField()
  justification_status = models.IntegerField(choices=[(e.value, e.name) for e in JustificationStatus])
  reason_decline = models.TextField(null=True)

  # Relacion de muchos a uno con User
  action_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, related_name='action_by_user')

  # Relacion de muchos a uno con User
  user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='justification_user')

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.id)