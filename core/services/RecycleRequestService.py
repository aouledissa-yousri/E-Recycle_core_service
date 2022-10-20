from core.helpers import RequestHelper
from core.models import RecycleRequest, Citizen, Material


class RecycleRequestService: 
    

    @staticmethod
    def makeRecycleRequest(request):
        recycleRequestData = RequestHelper.getRequestBody(request)

        try: 
            recycleRequest = RecycleRequest()
            recycleRequest.setData(recycleRequestData)
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
