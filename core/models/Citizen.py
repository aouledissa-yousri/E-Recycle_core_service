from django.db import models
from UserManagement.models import *


class Citizen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length = 255, default = '')
    lastname = models.CharField(max_length = 255, default = '')
