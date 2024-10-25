from rest_framework import serializers
from .models import Book
from firebase_admin import storage
from authentication.models import UserProfile

class BookSerializer(serializers.ModelSerializer):
    book_url = serializers.SerializerMethodField()
    owner_username = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'genre', 'condition', 'availability_status', 
                  'latitude', 'longitude', 'owner', 'owner_username', 'book_url', 'book_path']

    def get_book_url(self, obj):
        if obj.book_path:
            bucket = storage.bucket()
            blob = bucket.blob(obj.book_path)
            signed_url = blob.public_url
            return signed_url
        return None

    def get_owner_username(self, obj):
        try:
            user_profile = UserProfile.objects.get(uuid=obj.owner)
            return user_profile.username
        except UserProfile.DoesNotExist:
            return None

class BookSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'condition', 'availability_status', 'longitude', 'latitude']