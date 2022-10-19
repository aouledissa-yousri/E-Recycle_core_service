from django.urls import path
from .controllers import *



urlpatterns = [

    #citizen paths
    path("signUp/", CitizenController.signUp),

    path("login/", CitizenController.login),
    path("logout/", CitizenController.logout),
    path("logoutAllSessions/", CitizenController.logoutAllSessions),
    path("logoutAllOtherSessions/", CitizenController.logoutAllOtherSessions),

    path("confirmAccount/", CitizenController.confirmAccount),

    path("enableTwoFactorAuth/", CitizenController.enableTwoFactorAuth),
    path("disableTwoFactorAuth/", CitizenController.disableTwoFactorAuth),
    path("twoFactorAuth/", CitizenController.twoFactorAuth),


    path("requestPasswordReset/", CitizenController.requestPasswordReset)





    
]