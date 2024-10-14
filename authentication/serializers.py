from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class EmailOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

class EmailRegisterVerifySerializer(serializers.Serializer):
    uuid = serializers.CharField()
    otp = serializers.IntegerField()

class RegisterAccountSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    reading_preferences = serializers.CharField()
    favorite_genres = serializers.CharField()

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        reading_preferences = validated_data.get('reading_preferences', instance.reading_preferences)
        favorite_genres = validated_data.get('favorite_genres', instance.favorite_genres)
        instance.user_registered = True
        instance.save()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class ForgetPasswordChangeSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    otp = serializers.IntegerField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['uuid', 'username', 'full_name', 'email', 'favorite_genres', 'reading_preferences']

class UpdatePushNotificationTokenSerializer(serializers.Serializer):
    push_notification_token = serializers.CharField()