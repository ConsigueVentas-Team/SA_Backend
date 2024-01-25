from django.db import models
from api.model.JustificationStatusModel import JustificationStatus
from api.model.UserModel import User

class Justification(models.Model):
  justification_date = models.DateField()
  reason = models.TextField()
  evidence = models.CharField(max_length=150)
  justification_type = models.BooleanField()

  # Relacion de uno a uno con JustificationStatus
  justification_status = models.OneToOneField(JustificationStatus, on_delete = models.CASCADE)

  # Relacion de muchos a uno con User
  user = models.ForeignKey(User, on_delete = models.CASCADE)

  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.id()