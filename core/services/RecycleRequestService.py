from core.helpers import RequestHelper
from core.models import RecycleRequest, Citizen, Material
from UserManagement.Controllers import TokenController


class RecycleRequestService: 
    

    @staticmethod
    def makeRecycleRequest(request):
        recycleRequestData = RequestHelper.getRequestBody(request)

        try: 
            recycleRequest = RecycleRequest()
            recycleRequest.setData(recycleRequestData, request)
            recycleRequest.save()

            return {"message": "recycle request has been successfully submitted" }
        
        except Citizen.DoesNotExist:
            return {"message": "your account does not exist"}
        
        except Material.DoesNotExist:
            return {"message": "material doess not exist"}
        
        except KeyError:
            return {"message": "invalid parameters"}
    

    def withdrawRecycleRequest(request):

        recycleRequestData = RequestHelper.getRequestBody(request)

        try:
            RecycleRequest.objects.get(id = recycleRequestData["id"]).delete()
            return {"message": "Recycle Request has been deleted successfully"}
        
        except RecycleRequest.DoesNotExist:
            return {"message": "Recycle Request not found"}
    

    def getRecycleRequests(request):
        try:
            recycleRequests = RecycleRequest.objects.filter(citizen_id = Citizen.objects.get(user_id = TokenController.decodeToken(request.headers["Token"])["id"]).id)
            recycleRequestsData = [recycleRequest.getData() for recycleRequest in recycleRequests]
            return recycleRequestsData
        
        except RecycleRequest.DoesNotExist:
            return {"message": "You didn't make any recycle requests"}
