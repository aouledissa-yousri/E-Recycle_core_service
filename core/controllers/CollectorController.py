from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.decorators import checkAccessToken
from core.services import CollectorService

class CollectorController: 
    
    @api_view(["POST"])
    @staticmethod
    def signUp(request):
        return JsonResponse({"message" : CollectorService.signUp(request)})
    

    @api_view(["POST"])
    @staticmethod
    def login(request):
        return JsonResponse(CollectorService.login(request))
    
    @api_view(["DELETE"])
    @staticmethod
    @checkAccessToken
    def logout(request):
        return JsonResponse(CollectorService.logout(request))

    
    @api_view(["DELETE"])
    @staticmethod
    @checkAccessToken
    def logoutAllSessions(request):
        return JsonResponse(CollectorService.logoutAllSessions(request))

    
    @api_view(["DELETE"])
    @staticmethod
    @checkAccessToken
    def logoutAllOtherSessions(request):
        return JsonResponse(CollectorService.logoutAllOtherSessions(request))
    

    @api_view(["PATCH"])
    @staticmethod
    def confirmAccount(request):
        return JsonResponse(CollectorService.confirmAccount(request))
    

    @api_view(["PATCH"])
    @staticmethod
    @checkAccessToken
    def enableTwoFactorAuth(request):
        return JsonResponse(CollectorService.manageTwoFactorAuth(request))
    

    @api_view(["PATCH"])
    @checkAccessToken
    @staticmethod
    def disableTwoFactorAuth(request):
        return JsonResponse(CollectorService.manageTwoFactorAuth(request))
    
    @api_view(["PATCH"])
    @staticmethod
    def twoFactorAuth(request):
        return JsonResponse(CollectorService.twoFactorAuth(request))
    

    @api_view(["POST"])
    @staticmethod
    def requestPasswordReset(request):
        return JsonResponse(CollectorService.requestPasswordReset(request))
    

    @api_view(["DELETE"])
    def checkPasswordResetCode(request):
        return JsonResponse(CollectorService.checkPasswordResetCode(request))
    
    @api_view(["PATCH"])
    def resetPassword(request):
        return JsonResponse(CollectorService.resetPassword(request))
    

    @api_view(["PATCH"])
    @checkAccessToken
    def changePassword(request):  
        return JsonResponse(CollectorService.changePassword(request))


    @api_view(["GET"])
    def googleLoginGateway(request):
        return JsonResponse(CollectorService.googleLoginGateway()) 
    

    @api_view(["GET"])
    def googleLogin(request):
        return JsonResponse(CollectorService.googleLogin(request))
    

    @api_view(["GET"])
    def facebookLoginGateway(request):
        return JsonResponse(CollectorService.facebookLoginGateway())
    

    @api_view(["GET"])
    def facebookLogin(request):
        return JsonResponse(CollectorService.facebookLogin(request))
    
    
    
