from rest_framework import serializers, exceptions
from otpauth.models import OTPSeed
import pyotp
import otpauth

# For accessing / modifying the data
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPSeed
        fields = ('name', 'realm', 'seed')
        read_only_fields = ('seed',)

    def create(self, validated_data):
        validated_data['seed'] = pyotp.random_base32()
        return OTPSeed.objects.create(**validated_data)

# For parsing authentication
class TokenSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    token = serializers.CharField(max_length=128)
    realm = serializers.CharField(max_length=128)

    token_name = 'token'
    name_name = 'name'
    realm_name = 'realm'

    def save(self):
        token_in = self.validated_data.get(self.token_name)
        name_in =  self.validated_data.get(self.name_name)
        realm_in =  self.validated_data.get(self.realm_name)

        print("auth: {} {} {} ({} {} {} -- {})".format(token_in, name_in, realm_in, self.token_name, self.name_name, self.realm_name, self.validated_data))

        # 1. Verify that the connection might authenticate
        try:
            db_instance = otpauth.models.OTPSeed.objects.get(name=name_in, realm=realm_in)
        except (OTPSeed.MultipleObjectsReturned, OTPSeed.DoesNotExist):
            raise exceptions.AuthenticationFailed()

        totp = pyotp.TOTP(db_instance.seed)

        if not totp.verify(token_in, valid_window=3):
            raise exceptions.AuthenticationFailed()

        return (db_instance, token_in)

# For verifying a token
class VerifySerializer(TokenSerializer):
    verifyname = serializers.CharField(max_length=128)
    verifytoken = serializers.CharField(max_length=128)
    verifyrealm = serializers.CharField(max_length=128)

    token_name = 'verifytoken'
    name_name = 'verifyname'
    realm_name = 'verifyrealm'
