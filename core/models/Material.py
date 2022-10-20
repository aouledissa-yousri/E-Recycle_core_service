from django.db import models
from ..helpers import RequestHelper


class Material(models.Model): 
    type = models.CharField(max_length = 255, default = '', unique = True)


    def getData(self):
        return {
            "id": self.id,
            "type": self.type
        }
    
    def setData(self, data):
        self.type = data["type"]
    

    
        
        