from rest_framework.serializers import ModelSerializer
from dbuserapp.models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


