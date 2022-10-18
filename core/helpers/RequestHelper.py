import json

class RequestHelper: 

    #get resuest body
    @staticmethod
    def getRequestBody(request):
        return json.loads(request.body) 