from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.services import CitizenService

class CitizenController: 
    
    @api_view(["POST"])
    @staticmethod
    def signUp(request):
        return JsonResponse({"message" : CitizenService.signUp(request)})
    
    
