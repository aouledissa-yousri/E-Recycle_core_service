from rest_framework import serializers 
from .models import Citizen, Material

class CitizenSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Citizen
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Material
        fields = "__all__"