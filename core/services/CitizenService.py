from threading import Thread
from core.models import Citizen
from core.helpers import RequestHelper, CodeHelper, CredentialsHelper, HashHelper
from UserManagement.models import GenericUser, ConfirmationCode, User, Token
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
        
        
        return CitizenService.login(data)
                
        
    
    @staticmethod
    def login(request):

        data = RequestHelper.getRequestBody(request)

        try: 
            #search for user in database
            credentials = CredentialsHelper(data)
            account = GenericUser.login(credentials)


            #check if user account is not verfied
            if not account.verified:
                return CitizenService.sendConfirmationEmail(credentials.getData(), request)
            
            

            #check if username (or email) and password are correct get user data and access token 
            elif account.password == HashHelper.encryptPassword(credentials.password, account.salt) and (not account.isBlocked()):

                #restart login authorized tries
                account.restartTries()

                #create session and get citizen additional data
                return CitizenService.fetchCitizenData(account)


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
    


    #log out 
    @staticmethod 
    def logout(request):
        TokenController.deleteToken(request.headers["Token"])
        return {"message": "logged out"}


    #logout from all sessions 
    @staticmethod 
    def logoutAllSessions(request):
        decodedToken = TokenController.decodeToken(request.headers["Token"])

        try: 
            user = User.objects.get(id = decodedToken["id"])
            Token.objects.filter(user_id = user.id).delete()
            return {"message": "logged out from all sessions"}
        
        except User.DoesNotExist: 
            return {"message": "user not found"}
    

    @staticmethod 
    def logoutAllOtherSessions(request):
        decodedToken = TokenController.decodeToken(request.headers["Token"]) 

        try: 
            user = User.objects.get(id = decodedToken["id"])
            Token.objects.filter(user_id = user.id).exclude(token = request.headers["Token"]).delete()
            return {"message": "logged out from all other sessions"}
        
        except User.DoesNotExist: 
            return {"message": "user not found"}

    

    @staticmethod
    def confirmAccount(request):

        data = RequestHelper.getRequestBody(request)

        try:
            confirmationCode = ConfirmationCode.objects.get(code = data["code"])
            if confirmationCode.expirationDate >= timezone.now():
                user = GenericUser.objects.get(user_ptr_id = confirmationCode.user.id)
                user.verify()
                confirmationCode.delete()
                return CitizenService.fetchCitizenData(user)

            return {"message": "Confirmation code has been expired"}

        except ConfirmationCode.DoesNotExist:
            return {"message": "Confirmation code is not valid"}
        
        except KeyError: 
            return {"message": "Invalid parameters"}
        
    
    #enable two factor authentication
    @staticmethod 
    def manageTwoFactorAuth(request):
        data = TokenController.decodeToken(request.headers["Token"])

        #search for user 
        try: 
            if "enableTwoFactorAuth" in request.path:
                GenericUser.objects.filter(username = data["username"]).update(twoFactorAuth = True)
                return {"message": "Two factor authentication enabled"}

            elif "disableTwoFactorAuth" in request.path:
                GenericUser.objects.filter(username = data["username"]).update(twoFactorAuth = False)
                return {"message": "Two factor authentication disabled"}
        
        except GenericUser.DoesNotExist: 
            return {"message": "user does not exist"}
        
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
    
    
        

