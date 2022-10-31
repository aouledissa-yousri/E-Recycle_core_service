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

    #collector paths 
    path("collectorSignUp/", CollectorController.signUp),

    path("collectorLogin/", CollectorController.login),
    path("collectorLogout/", CollectorController.logout),
    path("collectorLogoutAllSessions/", CollectorController.logoutAllSessions),
    path("collectorLogoutAllOtherSessions/", CollectorController.logoutAllOtherSessions),

    path("collectorconfirmAccount/", CollectorController.confirmAccount),

    path("collectorEnableTwoFactorAuth/", CollectorController.enableTwoFactorAuth),
    path("collectorDisableTwoFactorAuth/", CollectorController.disableTwoFactorAuth),
    path("collectorTwoFactorAuth/", CollectorController.twoFactorAuth),


    path("collectorRequestPasswordReset/", CollectorController.requestPasswordReset),
    path("collectorCheckPasswordResetCode/", CollectorController.checkPasswordResetCode),
    path("collectorResetPassword/", CollectorController.resetPassword),
    path("collectorChangePassword/", CollectorController.changePassword),


    path("collectorGoogleLoginGateway/", CollectorController.googleLoginGateway),
    path("collectorGoogleLogin/", CollectorController.googleLogin),

    path("collectorFacebookLoginGateway/", CollectorController.facebookLoginGateway),
    path("collectorFacebookLogin/", CollectorController.facebookLogin),





    #material paths
    path("addMaterial/", MaterialController.addMaterial),
    path("getMaterials/", MaterialController.getMaterials),



    #recycle request paths
    path("makeRecycleRequest/", RecycleRequestController.makeRecycleRequest),
    path("reserveRecycleRequest/", RecycleRequestController.reserveRecycleRequest),
    path("submitRecycleRequest/", RecycleRequestController.submitRecycleRequest),

    path("withdrawRecycleRequest/", RecycleRequestController.withdrawRecycleRequest),
    path("getRecycleRequests/", RecycleRequestController.getRecycleRequests)
]