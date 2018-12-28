from rest_framework import serializers, exceptions
from user_management.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'email', 'password')