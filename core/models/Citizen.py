from django.db import models
from UserManagement.models import User
from UserManagement.serializers import *
from ..helpers import RequestHelper
from ..serializers import CitizenSerializer


class Citizen(models.Model):

    user: User = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length = 255, default = '')
    lastname = models.CharField(max_length = 255, default = '')
    
    def getData(self):

        return {
            "user_profile": self.user.getData(),
            "name": self.name,
            "lastname": self.lastname
        }
    
    def getAllData(self):

        data = {
            "user": self.user,
        }

        data["name"] = self.name 
        data["lastname"] = self.lastname

        return data
    

    def setData(self, data): 
        self.user = data["user"]
        self.name = data["name"]
        self.lastname = data["lastname"]
    
    
    # save user profile data
    def createUserProfile(self, userType, request):
        userProfile = RequestHelper.getRequestBody(request)

        if userType == "generic":

            user = GenericUser()
            user.setData(userProfile["user_profile"])
            user = GenericUserSerializer(data = user.getAllUserData())

            if user.is_valid():
                user.save()
                return "Account created successfully"

            try:
                GenericUser.objects.get(username = userProfile["user_profile"]["username"])
                return "Account already exists"

            except GenericUser.DoesNotExist:
                return "Account creation failed"
        
            except KeyError: 
                return "Invalid parameters"
        
        return "Nothing"

            
    

    def saveInstance(self, userType ,request):

        if userType == "generic":

            result = self.createUserProfile("generic", request)

            if result == "Account created successfully":
                
                citizenData = RequestHelper.getRequestBody(request)

                self.setData({
                    "user" : GenericUser.objects.get(username = citizenData["user_profile"]["username"]),
                    "name": citizenData["name"],
                    "lastname": citizenData["lastname"]
                })

                citizen = CitizenSerializer(data = self.getAllData())

                print(citizen.initial_data)
                print(self.getAllData())

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
        

