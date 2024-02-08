from django.db import models
from api.enums import JustificationStatus
from api.model.UserModel import User

class Justification(models.Model):
  justification_date = models.DateField()
  reason = models.TextField()
  evidence = models.ImageField(max_length=200)
  justification_type = models.BooleanField()
  justification_status = models.IntegerField(choices=[(e.value, e.name) for e in JustificationStatus])
  reason_decline = models.TextField(null=True)

  # Relacion de muchos a uno con User
  action_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, related_name='action_by_user')

  # Relacion de muchos a uno con User
  user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='justification_user')

  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.id)