from django.db import models


class Material(models.Model): 
    username = models.CharField(max_length = 255, default = '', unique = True)