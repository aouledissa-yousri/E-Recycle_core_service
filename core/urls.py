from django.urls import path
from core.controllers import *



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


    path("requestPasswordReset/", CitizenController.requestPasswordReset),
    path("checkPasswordResetCode/", CitizenController.checkPasswordResetCode),
    path("resetPassword/", CitizenController.resetPassword),
    path("changePassword/", CitizenController.changePassword),


    path("googleLoginGateway/", CitizenController.googleLoginGateway),
    path("googleLogin/", CitizenController.googleLogin),

    path("facebookLoginGateway/", CitizenController.facebookLoginGateway),
    path("facebookLogin/", CitizenController.facebookLogin),





    #material paths
    path("addMaterial/", MaterialController.addMaterial),
    path("getMaterials/", MaterialController.getMaterials),



    #recycle request paths
    path("makeRecycleRequest/", RecycleRequestController.makeRecycleRequest),
    path("withdrawRecycleRequest/", RecycleRequestController.withdrawRecycleRequest),
    path("getRecycleRequests/", RecycleRequestController.getRecycleRequests)
]