from threading import Thread
from core.models import Citizen
from core.helpers import RequestHelper, CodeHelper, CredentialsHelper, HashHelper
from UserManagement.models import GenericUser, ConfirmationCode, User
from UserManagement.serializers import ConfirmationCodeSerializer
from UserManagement.Controllers import TokenController
from Global.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.utils import timezone
import random




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

            #citizen = CitizenSerializer(data = citizen.getAllData())


            #if citizen.is_valid():

            citizen.save()
            return "Account created successfully"
                
        return result

    
    @staticmethod 
    def sendConfirmationEmail(userProfile, request):
        confirmationCode = CodeHelper.generateCode()
        message = "Hello "+ userProfile["username"] + ",\nThank you for signining up Here is your confirmation code: "+ confirmationCode
        

        code = ConfirmationCode()
        code.setData(confirmationCode, GenericUser.objects.get(username = userProfile["username"]), CodeHelper.generateExpirationDate(request))
        code = ConfirmationCodeSerializer(data = code.getData())

        if code.is_valid():
            ConfirmationCode.objects.filter(user_id = GenericUser.objects.get(username = userProfile["username"]).id).delete()
            code.save()
            
            EmailMessage("Email Confirmation", message, EMAIL_HOST_USER, [userProfile["email"]]).send()

            return {"message": "A confirmation code has been sent to your email"}

        return {"message": "Confirmation code has not been sent"}
    


    @staticmethod
    def loginGateway(request): 

        data = RequestHelper.getRequestBody(request)

        #serch for user and get his email (to send a confirmation code or 2-factor authentication code without reading again from the database)
        try: 
            user = GenericUser.objects.get(username = data["username"])
            data["email"] = user.email
        
        #user with corresponding username does not exist
        except GenericUser.DoesNotExist:
            return {"message" : "User not found"}
        

        #if username is not provided
        except KeyError:

            #check if email is provided by the end-user
            try: 
                user = GenericUser.objects.get(email = data["email"])
                data["username"] = user.username

            #if neither email or username is provided
            except KeyError: 
                return {"message": "Invalid username or email"}
            
            #user with corresponding email does not exist
            except GenericUser.DoesNotExist:
                return {"message" : "User not found"}
            
        
        
        #if account is not verified send service
        '''if not user.verified:
            return CitizenService.sendConfirmationEmail(data, request)'''
        
        return CitizenService.login(data)
                
        
    
    @staticmethod
    def login(data):

        try: 
            #search for user in database
            credentials = CredentialsHelper(data)
            account = GenericUser.login(credentials)
            

            #check if username (or email) and password are correct get user data and access token 
            if account.password == HashHelper.encryptPassword(credentials.password, account.salt) and (not account.isBlocked()):

                #restart login authorized tries
                account.restartTries()

                #create session and get citizen additional data
                return CitizenService.fetchCitizenData(account)


            print(HashHelper.encryptPassword(HashHelper.hashPassword(credentials.password), account.salt))
            print(account.password)

            #if password is wrong decrement possible login attempts/tries 
            account.decrementTries()

            #if user provides a wrong password for the third time block his account for a specefic period of time
            if account.getTries() < 1 :
                if not account.isBlocked():
                    account.block()
                    Thread(target = account.unblock).start()
                
                 #if account is blocked temporarily
                return {"message": "your account is temporarily blocked please try again later!"}

            #if password is wrong
            return {"message":"password is wrong"}
        
         #if user is not found
        except GenericUser.DoesNotExist : 
            return {"message":"user not found"}
        
        #request payload is invalid
        except KeyError: 
            return {"message": "invalid parameters"}
    

    @staticmethod
    def confirmAccount(request):

        data = RequestHelper.getRequestBody(request)
        user = GenericUser.objects.get(username = data["username"])

        try:
            confirmationCode = ConfirmationCode.objects.get(code = data["code"], user_id = user.id)
            if confirmationCode.expirationDate >= timezone.now():
                user.verify()
                confirmationCode.delete()
                return CitizenService.fetchCitizenData(user)

            return {"message": "Confirmation code has been expired"}

        except ConfirmationCode.DoesNotExist:
            return {"message": "Confirmation code is not valid"}
        
        except KeyError: 
            return {"message": "Invalid parameters"}
    
    

            
    @staticmethod
    def fetchCitizenData(account: User):

        token = CitizenService.createSession(account)

        citizen = Citizen()
        citizen.setData({
            "user": account,
            "name": Citizen.objects.get(user_id = account.id).name,
            "lastname": Citizen.objects.get(user_id = account.id).lastname
        })

        return {
            "message": "success",
            "user": citizen.getData(),
            "token": token
        }
    

    @staticmethod
    def createSession(account: User):

        #generate access token
        token = TokenController.generateToken({
            "username": account.username,
            "id": account.id,
            "number": random.randint(0, 10000000000000000)
        })

        #save token in database to act as an active user session id
        TokenController.saveToken(token, account)

        return token
        

