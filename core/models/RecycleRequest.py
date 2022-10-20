from django.db import models 
from django.utils import timezone
from .Citizen import Citizen
from .Material import Material



class RecycleRequest(models.Model):

    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, default=0)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default=0)
    quantity = models.FloatField(default = 3)
    unit = models.CharField(max_length = 255, default = '')
    location = models.CharField(max_length = 255, default = '')
    dateSubmitted = models.DateTimeField(default = timezone.now())
    status = models.CharField(max_length = 255, default = '')


    def setData(self, materialData):
        self.citizen = Citizen.objects.get(username = materialData["username"])
        self.material = Material.objects.get(type = materialData["material"])
        self.quantity = materialData["quantity"]
        self.unit = materialData["unit"]
        self.location = materialData["location"]
        self.dateSubmitted = materialData["dateSubmitted"]
        self.status = "pending"
    

    def getData(self):
        
        return {
            "citizen": self.citizen,
            "material": self.material,
            "quantity": self.quantity,
            "unit": self.unit,
            "location": self.location,
            "dateSubmitted": self.dateSubmitted,
            "status": self.status
        }


