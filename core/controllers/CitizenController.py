from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.services import CitizenService
from core.decorators import checkAccessToken

class CitizenController: 
    
    @api_view(["POST"])
    @staticmethod
    def signUp(request):
        return JsonResponse({"message" : CitizenService.signUp(request)})
    

    @api_view(["POST"])
    @staticmethod
    def login(request):
        return JsonResponse(CitizenService.login(request))
    
    @api_view(["DELETE"])
    @staticmethod
    @checkAccessToken
    def logout(request):
        return JsonResponse(CitizenService.logout(request))

    
    @api_view(["DELETE"])
    @staticmethod
    @checkAccessToken
    def logoutAllSessions(request):
        return JsonResponse(CitizenService.logoutAllSessions(request))

    
    @api_view(["DELETE"])
    @staticmethod
    @checkAccessToken
    def logoutAllOtherSessions(request):
        return JsonResponse(CitizenService.logoutAllOtherSessions(request))
    

    @api_view(["PATCH"])
    @staticmethod
    def confirmAccount(request):
        return JsonResponse(CitizenService.confirmAccount(request))
    

    @api_view(["PATCH"])
    @staticmethod
    @checkAccessToken
    def enableTwoFactorAuth(request):
        return JsonResponse(CitizenService.manageTwoFactorAuth(request))
    

    @api_view(["PATCH"])
    @checkAccessToken
    @staticmethod
    def disableTwoFactorAuth(request):
        return JsonResponse(CitizenService.manageTwoFactorAuth(request))
    
    @api_view(["PATCH"])
    @staticmethod
    def twoFactorAuth(request):
        return JsonResponse(CitizenService.twoFactorAuth(request))
    

    @api_view(["POST"])
    @staticmethod
    def requestPasswordReset(request):
        return JsonResponse(CitizenService.requestPasswordReset(request))
    

    @api_view(["DELETE"])
    def checkPasswordResetCode(request):
        return JsonResponse(CitizenService.checkPasswordResetCode(request))
    
    @api_view(["PATCH"])
    def resetPassword(request):
        return JsonResponse(CitizenService.resetPassword(request))
    

    @api_view(["PATCH"])
    @checkAccessToken
    def changePassword(request):  
        return JsonResponse(CitizenService.changePassword(request))


    @api_view(["GET"])
    def googleLoginGateway(request):
        return JsonResponse(CitizenService.googleLoginGateway()) 
    

    @api_view(["GET"])
    def googleLogin(request):
        return JsonResponse(CitizenService.googleLogin(request))
    

    @api_view(["GET"])
    def facebookLoginGateway(request):
        return JsonResponse(CitizenService.facebookLoginGateway())
    

    @api_view(["GET"])
    def facebookLogin(request):
        return CitizenService.facebookLogin(request)
    
    
    
