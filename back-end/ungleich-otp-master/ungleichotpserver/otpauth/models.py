from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class OTPSeed(AbstractUser):
    id       = models.AutoField(primary_key=True)
    name     = models.CharField(max_length=128)
    realm    = models.CharField(max_length=128)
    seed     = models.CharField(max_length=128)

    class Meta:
        unique_together = (('name', 'realm'),)

    def __str__(self):
        return "'{}'@{}".format(self.name, self.realm)

#     @classmethod
#     def get_username(cls):
#         pass

#     @classmethod
#     def check_password(cls, raw_password):
#         """ receives a time based token"""
#         pass

#     @classmethod
#     def has_usable_password(cls):
#         pass


from rest_framework import exceptions
from rest_framework import authentication
from otpauth.models import OTPSeed
from otpauth.serializer import TokenSerializer

class OTPAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        data = request.data
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            print("trying to save... {}".format(serializer))
            user, token = serializer.save()
        else:
            raise exceptions.AuthenticationFailed()

        return (user, token)
