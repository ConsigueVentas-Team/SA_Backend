from django.db import models

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    def __str__(self):
        return str(self.name)