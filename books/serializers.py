import time
from rest_framework import serializers

from authentication.models import UserProfile
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def get_owner_name(self, obj):
        try:
            user_profile = UserProfile.objects.get(uuid=obj.owner)
            return user_profile.username
        except UserProfile.DoesNotExist:
            return None

class BookSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'condition', 'availability_status', 'longitude', 'latitude', 'created_on']

    def create(self, validated_data):
        validated_data['created_on'] = int(time.time()) 
        return super().create(validated_data)

