from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import UserProfile
from .serializers import *
from .utils import *
import random
import uuid

class EmailRegisterOtpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user_exists = UserProfile.objects.filter(email=email).exists()
            if user_exists:
                response_data = {'msg': 'present'}
            else:
                otp = random.randint(111111, 999999)
                new_uuid = uuid.uuid4()
                new_user = UserProfile.objects.create(
                    uuid=new_uuid,
                    email=email,
                    email_verified=False,
                    otp=otp,
                    is_active=True
                )
                new_user.save()
                send_register_email_otp(email, otp)
                response_data = {'uuid': new_uuid}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class EmailRegisterVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailRegisterVerifySerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            otp = serializer.validated_data['otp']
            user_instance = UserProfile.objects.filter(uuid=uuid, otp=otp).first()
            if user_instance:
                user_instance.email_verified = True
                user_instance.save()
                response_data = {'msg': 'ok'}
            else:
                response_data = {'msg': 'invalid OTP'}

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserAccount(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterAccountSerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            user_instance = UserProfile.objects.filter(uuid=uuid).first()
            if user_instance:
                serializer.update(user_instance, serializer.validated_data)
                response_data = {'msg':'ok'}
            else:
                response_data = {'msg':'nok'}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgetPassowrdOtp(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user_exists = UserProfile.objects.filter(email=email).exists()
            if user_exists:
                user_instance = UserProfile.objects.filter(email=email).first()
                otp = random.randint(111111, 999999)
                user_instance.otp = otp
                user_instance.save()
                send_forget_password_email_otp(email, otp)
                response_data = {'uuid': user_instance.uuid}
            else:
                response_data = {'msg': 'not present'}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordChange(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgetPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            otp = serializer.validated_data['otp']
            password = serializer.validated_data['password']
            user_instance = UserProfile.objects.filter(uuid=uuid, otp=otp).first()
            if user_instance:
                user_instance.email_verified = True
                user = User.objects.get(username=user_instance.username)
                user.set_password(password)
                user.save()
                response_data = {'msg': 'ok'}
            else:
                return Response({'msg': 'nok'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckUserTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        token_string = request.auth.key
        token = Token.objects.get(key=token_string)
        user = request.user
        if token.user == user:
            if token.created > timezone.now() - timedelta(days=1):
                response_data = {'msg': 'ok'}
            else:
                response_data = {'msg': 'nok'}
        else:
            response_data = {'msg': 'nok'}
        return Response(response_data, status=status.HTTP_200_OK)

class UserDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(username=request.user.username)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
