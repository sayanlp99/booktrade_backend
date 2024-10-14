from django.urls import path
from .views import *
from rest_framework.authtoken import views


urlpatterns = [
    path('sendEmailOtp', EmailRegisterOtpView.as_view(), name='email_register_otp'),
    path('verifyEmailOtp', EmailRegisterVerifyView.as_view(), name='email_register_verify'),
    path('registerUser', RegisterUserAccount.as_view(), name='user_register'),
    path('forgetPasswordOtp', ForgetPassowrdOtp.as_view(), name='forget_password_otp'),
    path('forgetPasswordChangePassword', ForgetPasswordChange.as_view(), name='forget_password_change'),
    path('login', views.obtain_auth_token, name='login'),
    path('checkUserToken', CheckUserTokenView.as_view(), name='check_user_token'),
    path('userDetails', UserDetailsView.as_view(), name='user_details'),
]
