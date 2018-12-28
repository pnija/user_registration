from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from random import choice
from string import ascii_uppercase

from user_management.serializers import UserSerializer
from user_management.models import Users
from otpauth.serializer import OTPSerializer
from otpauth.models import OTPSeed


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        data = {'name': request.data['name'],
                'realm': 'ungleich-admin',
                'seed': ''.join(choice(ascii_uppercase) for i in range(12))}
        otp_serializer = OTPSerializer(data=data)
        if otp_serializer.is_valid() and serializer.is_valid():
            otp_serializer.save()
            serializer.save()
            return Response({'status': 'OK'})

        return JsonResponse(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def login(self, request):
        data = request.data
        try:
            Users.objects.get(name=data['name'], password=data['password'])
            otp_seed = OTPSeed.objects.get(name=data['name'])
            return Response({'name':data['name'], 'realm': otp_seed.realm, 'seed':otp_seed.seed})
        except Exception as exp:
            return JsonResponse({'Exception':exp}, status=400)