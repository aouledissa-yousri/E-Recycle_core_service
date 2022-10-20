from threading import Thread
from core.models import Citizen
from core.helpers import RequestHelper, CodeHelper, CredentialsHelper, HashHelper
from UserManagement.models import GenericUser, ConfirmationCode, User, Token, TwoFactorAuthCode, PasswordResetCode, GoogleUser, FacebookUser
from UserManagement.serializers import ConfirmationCodeSerializer, TwoFactorAuthCodeSerializer, PasswordResetCodeSerializer
from UserManagement.Controllers import TokenController, GoogleUserController, FacebookUserController
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
    def login(request):

        data = RequestHelper.getRequestBody(request)

        try: 
            #search for user in database
            credentials = CredentialsHelper(data)
            account = GenericUser.login(credentials)


            
            

            #check if username (or email) and password are correct get user data and access token 
            if account.password == HashHelper.encryptPassword(credentials.password, account.salt) and (not account.isBlocked()):

                #restart login authorized tries
                account.restartTries()

                #check if user account is not verfied
                if not account.verified:
                    return CitizenService.sendConfirmationEmail(credentials.getData(), request)

                #check if two factor authentication is enabled
                elif account.twoFactorAuth: 
                    return CitizenService.sendTwoFactorAuthCode(credentials.getData(), request)
            

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
    

    #logout from all other sessions
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


    
    #send two factor authentication code to the user's email address
    @staticmethod 
    def sendTwoFactorAuthCode(userProfile, request):
        twoFactorAuthCode = CodeHelper.generateCode()
        message = "Hello "+ userProfile["username"] + ",\nHere is your 2-step verification code : "+ twoFactorAuthCode

        twoFactorCode = TwoFactorAuthCode()
        twoFactorCode.setData(twoFactorAuthCode, GenericUser.objects.get(username = userProfile["username"]), CodeHelper.generateExpirationDate(request))
        twoFactorCode = TwoFactorAuthCodeSerializer(data = twoFactorCode.getData())

        if twoFactorCode.is_valid():

            TwoFactorAuthCode.objects.filter(user_id = GenericUser.objects.get(username = userProfile["username"]).id).delete()
            twoFactorCode.save()
            EmailMessage("2-Step verification code", message, EMAIL_HOST_USER, [userProfile["email"]]).send()
                
            return {"message": "Verification code has been sent to your email address"}

        return {"message": "Verification code has not been sent"}
    

    #login with 2 factor authentication code
    @staticmethod
    def twoFactorAuth(request):

        data = RequestHelper.getRequestBody(request)

        try:
            twoFactorAuthCode = TwoFactorAuthCode.objects.get(code = data["code"])
            if twoFactorAuthCode.expirationDate >= timezone.now():
                user = GenericUser.objects.get(user_ptr_id = twoFactorAuthCode.user.id)
                user.verify()
                twoFactorAuthCode.delete()
                return CitizenService.fetchCitizenData(user)

            return {"message": "Confirmation code has been expired"}

        except TwoFactorAuthCode.DoesNotExist:
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
    


    @staticmethod
    def requestPasswordReset(request):
        userProfile = RequestHelper.getRequestBody(request)

        if userProfile.get("username"):
            user = GenericUser.objects.get(username=userProfile["username"]).getData()
        elif userProfile.get("email"):
            user = GenericUser.objects.get(username=userProfile["email"]).getData()
        else: 
            return {"message": "Invalid parameters"}
        

        return CitizenService.sendPasswordResetCode(user, request)
    

    @staticmethod 
    def sendPasswordResetCode(userProfile, request):
        passwordResetCode = CodeHelper.generateCode()
        message = "Hello "+ userProfile["username"] + ",\n Here is your password reset code : "+ passwordResetCode

        passwordReset = PasswordResetCode()
        passwordReset.setData(passwordResetCode, GenericUser.objects.get(username = userProfile["username"]), CodeHelper.generateExpirationDate(request))
        passwordReset = PasswordResetCodeSerializer(data = passwordReset.getData())


        if passwordReset.is_valid():
            PasswordResetCode.objects.filter(user_id = GenericUser.objects.get(username = userProfile["username"]).id).delete()
            passwordReset.save()        

            EmailMessage("Password Reset Code", message, EMAIL_HOST_USER, [userProfile["email"]]).send()
                
            return {"message": "Passoword reset code has been sent"}

        return {"message": "Password reset code has not been sent"}
    


    @staticmethod
    def checkPasswordResetCode(request):
        data = RequestHelper.getRequestBody(request)

        try: 
            passwordResetCode = PasswordResetCode.objects.get(code = data["code"])
            if passwordResetCode.expirationDate >= timezone.now():
                user = GenericUser.objects.get(user_ptr_id = passwordResetCode.user.id)
                passwordResetCode.delete()
                return {
                    "message": "code is valid",
                    "username": user.username,
                    "email": user.email
                }

            return {"message": "Password reset code has been expired"}

        except PasswordResetCode.DoesNotExist:
            return {"message": "Passwored reset code is not valid"}
        
        except KeyError: 
            return {"message": "Invalid parameters"}
    

    @staticmethod
    def resetPassword(request):
        data = RequestHelper.getRequestBody(request)

        try: 
            user = GenericUser.objects.get(username = data['username'])
        
        except GenericUser.DoesNotExist:
            return {"message": "User does not exist"}
        
        except KeyError:

            try: 
                user = GenericUser.objects.get(username = data['email'])
            
            except GenericUser.DoesNotExist:
                return {"message": "User does not exist"}
            
            except KeyError:

                return {"message": "Invalid parameters"}
        
        user.changePassword(data['password'])
        return {"message": "Password changed"}
    

    @staticmethod
    def changePassword(request):
        data = RequestHelper.getRequestBody(request)
        userProfile = TokenController.decodeToken(request.headers["Token"])

        try:
            GenericUser.objects.get(username = userProfile["username"]).changePassword(data["password"])
            return {"message": "Password has been changed"}
        
        except GenericUser.DoesNotExist:
            return {"message": "User not found"}
    


    #redirect to google login page
    def googleLoginGateway():
        return GoogleUserController.googleLoginGateway()
    

    #google login 
    def googleLogin(request):
        googleUserData =  GoogleUserController.googleLogin(request)


        #seperate google account username to name and lastname 
        googleUserData["name"] = googleUserData["user"]["username"].split(" ")[0]
        googleUserData["lastname"] = googleUserData["user"]["username"].split(" ")[1]


        citizen = Citizen()
        citizen.setData({
            "user" : GoogleUser.objects.get(username = googleUserData["user"]["username"]),
            "name": googleUserData["name"],
            "lastname": googleUserData["lastname"]
        })

        citizen.save()


        return {
            "message": "success",
            "user": citizen.getData(),
            "token": googleUserData["token"]
        }
    

    #redirect to facebook login page
    def facebookLoginGateway():
        return FacebookUserController.facebookLoginGateway()
    

    #facebook login
    def facebookLogin(request):
        facebookUserData = FacebookUserController.facebookLogin(request)

        #seperate google account username to name and lastname 
        facebookUserData["name"] = facebookUserData["user"]["username"].split(" ")[0]
        facebookUserData["lastname"] = facebookUserData["user"]["username"].split(" ")[1]


        citizen = Citizen()
        citizen.setData({
            "user" : FacebookUser.objects.get(username = facebookUserData["user"]["username"]),
            "name": facebookUserData["name"],
            "lastname": facebookUserData["lastname"]
        })

        citizen.save()


        return {
            "message": "success",
            "user": citizen.getData(),
            "token": facebookUserData["token"]
        }