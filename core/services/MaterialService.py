from core.helpers import RequestHelper
from core.serializers import MaterialSerializer
from core.models import Material
from django.views import View


class MaterialService(object): 

    @staticmethod
    def addMaterial(request):

        material = Material()
        materialData = RequestHelper.getRequestBody(request)
        material.setData(materialData)
        material.save()

        return "Material has been added"
    


    @staticmethod
    def getMaterials(request):
        materials = Material.objects.all()
        materialData = [material.getData() for material in materials]
        return materialData
        