from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from django.http import JsonResponse
from otpauth.serializer import VerifySerializer, OTPSerializer
from otpauth.models import OTPSeed


class OTPVerifyViewSet(viewsets.ModelViewSet):
    serializer_class = OTPSerializer
    queryset = OTPSeed.objects.all()

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """the standard serializer above already verified that
        (name, realm, token) is valid.

        Now we inspect the verify-prefixed names and return ok,
        if they also verify
        """

        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'OK'})

        return JsonResponse(serializer.errors, status=400)
