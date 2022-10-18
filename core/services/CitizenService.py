from core.models import Citizen
from core.helpers import RequestHelper
from core.serializers import CitizenSerializer
from UserManagement.models import GenericUser

class CitizenService: 
    
    @staticmethod
    def createUserProfile(userType, request):
        citizen = Citizen()
        return citizen.createUserProfile(userType, request)
    

    @staticmethod
    def signUp(request):

        citizen = Citizen()
        result = CitizenService.createUserProfile("generic", request)

        if result == "Account created successfully":
            citizenData = RequestHelper.getRequestBody(request)

            citizen.setData({
                "user" : GenericUser.objects.get(username = citizenData["user_profile"]["username"]),
                "name": citizenData["name"],
                "lastname": citizenData["lastname"]
            })

            citizen = CitizenSerializer(data = citizen.getAllData())


            if citizen.is_valid():
                citizen.save()
                return "Account created successfully"
                
            try:
                Citizen.objects.get(id = self.id)
                return "Account already exists"

            except Citizen.DoesNotExist:
                return "Account creation failed"
        
            except KeyError: 
                return "Invalid parameters"
            
            
        return result
        