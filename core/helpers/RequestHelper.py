import json

class RequestHelper: 

    #get resuest body
    @staticmethod
    def getRequestBody(request):
        return json.loads(request.body)
    

    @staticmethod
    def requestParamsValid(request, keys: list):
        requestBody = RequestHelper.getRequestBody(request)

        for key in keys:
            if key not in requestBody.keys():
                return False
        
        return True