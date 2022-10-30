from django.db import models
from UserManagement.models import User
from UserManagement.serializers import *
from ..helpers import RequestHelper


class Collector(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length = 255, default = '')
    lastname = models.CharField(max_length = 255, default = '')
    RecycleRequests = list()
    
    

    def getData(self):


            return {
            "user_profile": self.user.getData(),
            "name": self.name,
            "lastname": self.lastname,
            "RecycleRequests" : self.RecycleRequests
        }
    
    def getAllData(self):

        data = {
            "user": self.user,
        }

        data["name"] = self.name 
        data["lastname"] = self.lastname
        data["RecycleRequests"] = self.RecycleRequests


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
                
                collectorData = RequestHelper.getRequestBody(request)

                self.setData({
                    "user" : GenericUser.objects.get(username = collectorData["user_profile"]["username"]),
                    "name": collectorData["name"],
                    "lastname": collectorData["lastname"]
                })

                collector = Collector()

                collector.setData(self)

                print(collector.initial_data)
                print(self.getAllData())

                collector.save()
            
            
            return result