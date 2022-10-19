from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.services import CitizenService

class CitizenController: 
    
    @api_view(["POST"])
    @staticmethod
    def signUp(request):
        return JsonResponse({"message" : CitizenService.signUp(request)})
    

    @api_view(["POST"])
    @staticmethod
    def login(request):
        return JsonResponse(CitizenService.login(request), safe=False)
    
    @api_view(["DELETE"])
    @staticmethod
    def logout(request):
        return JsonResponse(CitizenService.logout(request))

    
    @api_view(["DELETE"])
    @staticmethod
    def logoutAllSessions(request):
        return JsonResponse(CitizenService.logoutAllSessions(request))

    
    @api_view(["DELETE"])
    @staticmethod
    def logoutAllOtherSessions(request):
        return JsonResponse(CitizenService.logoutAllOtherSessions(request))
    

    @api_view(["PATCH"])
    @staticmethod
    def confirmAccount(request):
        return JsonResponse(CitizenService.confirmAccount(request), safe=False)
    
    
    
    
