from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'condition', 'availability_status']

