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
    

    @api_view(["DELETE"])
    @staticmethod
    @checkAccessToken
    def withdrawRecycleRequest(request):
        return JsonResponse(RecycleRequestService.withdrawRecycleRequest(request))


    @api_view(["POST"])
    @staticmethod
    @checkAccessToken
    def reserveRecycleRequest(request):
        return JsonResponse(RecycleRequestService.reserveRecycleRequest(request))


    @api_view(["POST"])
    @staticmethod
    @checkAccessToken
    def submitRecycleRequest(request):
        return JsonResponse(RecycleRequestService.submitRecycleRequest(request))




    @api_view(["GET"])
    @staticmethod
    @checkAccessToken
    def getRecycleRequests(request):
        return JsonResponse(RecycleRequestService.getRecycleRequests(request), safe = False)
    