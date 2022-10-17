from django.db import models


class Material(models.Model): 
    type = models.CharField(max_length = 255, default = '', unique = True)