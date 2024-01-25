from django.db import models

class JustificationStatus(models.Model):
  name = models.CharField(max_length=30)

  class Meta:
    db_table = 'api_justification_status'