from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.services import RecycleRequestService
from core.decorators import checkAccessToken

class RecycleRequestController: 
    

    @api_view(["POST"])
    @staticmethod
    @checkAccessToken
    def makeRecycleRequest(request):
        return JsonResponse(RecycleRequestService.makeRecycleRequest(request))
    

    @api_view(["POST"])
    @staticmethod
    @checkAccessToken
    def withdrawRecycleRequest(request):
        return JsonResponse(RecycleRequestService.withdrawRecycleRequest(request))
    