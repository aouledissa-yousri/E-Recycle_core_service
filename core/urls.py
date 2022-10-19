from django.urls import path
from .controllers import *



urlpatterns = [

    #citizen paths
    path("signUp/", CitizenController.signUp),
    path("login/", CitizenController.login),




    # material controller paths
    path("addMaterial/", MaterialController.addMaterial)
]