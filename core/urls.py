from django.urls import path
from .controllers import *



urlpatterns = [

    #citizen paths
    path("signUp/", CitizenController.signUp),




    # material controller paths
    path("addMaterial/", MaterialController.addMaterial)
]