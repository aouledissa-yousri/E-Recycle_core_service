

class UrlHelper: 

    #get base url 
    @staticmethod
    def getBaseUrl(request):
        baseUrl = str(request.build_absolute_uri()).replace(request.path, "")
        return baseUrl