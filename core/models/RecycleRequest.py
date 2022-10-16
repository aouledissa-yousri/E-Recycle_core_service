from django.db import models 
from datetime import datetime, timedelta
from .Citizen import Citizen
from .Material import Material



class RecycleRequest(models.Model):

    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, default=0)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default=0)
    quantity = models.FloatField(default = 3)
    unit = models.CharField(max_length = 255, default = '')
    location = models.CharField(max_length = 255, default = '')
    dateSubmitted = models.DateTimeField(default = datetime.now() + timedelta(minutes = 5))
    status = models.CharField(max_length = 255, default = '')


