from django.db import models
from user.models import User


class Receive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    value = models.FloatField(default=0)
    type = models.CharField(max_length=255)
    date = models.DateField()
