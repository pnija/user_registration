import json
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
        data = {'username':'user-' + request.data['name'],
                'name': request.data['name'],
                'realm': 'ungleich-admin',
                'seed': ''.join(choice(ascii_uppercase) for i in range(12))}
        otp_serializer = OTPSerializer(data=data)
        if otp_serializer.is_valid() and serializer.is_valid():
            otp_seed = OTPSeed(name=data['name'],
                               realm=data['realm'],
                               seed=data['seed'],
                               username=data['username'])
            otp_seed.save()
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
            return JsonResponse({'status': 'Invalid credentials'}, status=400)

    @action(detail=False, methods=['get'])
    def user_details(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        header = json.loads(header)
        name = header.get('name')
        realm = header.get('realm')
        seed = header.get('seed')
        
        try:
            otp_seed = OTPSeed.objects.get(name=name,
                                           realm=realm,
                                           seed=seed)
            if otp_seed:
                try:
                    user = Users.objects.get(name=name)
                except Exception as exp:
                    return JsonResponse({'Exception':str(exp)}, status=400)
                return Response({'name':user.name, 'email':user.email})
            return Response({'status': 'User details not found'})
        except Exception as exp:
            return JsonResponse({'status': 'Invalid credentials'}, status=400)

    @action(detail=False, methods=['post'])
    def update_details(self, request):
        data = request.data
        header = request.META.get('HTTP_AUTHORIZATION')
        header = json.loads(header)
        name = header.get('name')
        realm = header.get('realm')
        seed = header.get('seed')
        
        try:
            otp_seed = OTPSeed.objects.get(name=name,
                                           realm=realm,
                                           seed=seed)
            if otp_seed:
                new_name = data.get('name')
                new_email = data.get('email')
                try:
                    user = Users.objects.get(name=name)
                except Exception as exp:
                    return JsonResponse({'Exception':str(exp)}, status=400)
                otp_seed.name = new_name
                otp_seed.save()
                user.name = new_name
                user.email = new_email
                user.save()
                return Response({'status': 'OK', 'name':new_name})
            return Response({'status': 'User details updation failed'})
        except Exception as exp:
            return JsonResponse({'status': 'Invalid credentials'}, status=400)
