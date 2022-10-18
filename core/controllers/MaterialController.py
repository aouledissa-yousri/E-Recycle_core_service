from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.services import MaterialService

class MaterialController: 

    @api_view(["POST"])
    @staticmethod
    def addMaterial(request):
        return JsonResponse({"message": MaterialService.addMaterial(request)})
    
    