import time
import uuid
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Book
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from authentication.models import UserProfile
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from math import radians, cos, sin, sqrt, atan2
from rest_framework.decorators import action

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def list(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get('userId')
            if user_id:
                books = Book.objects.filter(owner=user_id)
            else:
                user_profile = UserProfile.objects.get(username=request.user.username)
                books = Book.objects.filter(owner=user_profile.uuid) 
            
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            image = request.FILES.get('image') 
            if image:
                serializer = BookSaveSerializer(data=request.data)
                if serializer.is_valid():
                    user_profile = UserProfile.objects.get(username=request.user.username)
                    bucket = storage.bucket()
                    book_id = str(uuid.uuid4())
                    book_path = f'books/images/{book_id}/{image.name}'
                    blob = bucket.blob(book_path)
                    blob.upload_from_file(image)
                    blob.make_public() 
                    book = serializer.save(owner=user_profile.uuid, created_on=int(time.time()), book_path=book_path)
                    return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_profile = UserProfile.objects.get(username=request.user.username)
            if instance.owner != user_profile.uuid:
                return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            serializer = BookSaveSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_profile = UserProfile.objects.get(username=request.user.username)
            if instance.owner != user_profile.uuid:
                return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            instance.delete()
            return Response({'message': 'Deleted the item from the Book list'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=False, methods=['get'], url_path='search', url_name='book_search')
    def search_books(self, request):
        keyword = request.query_params.get('q', '')
        genre = request.query_params.get('genre', '')
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        availability_status = request.query_params.get('available', '')
        query = Q()
        if keyword:
            query &= Q(title__icontains=keyword) | Q(author__icontains=keyword) | Q(genre__icontains=keyword)
        if genre:
            query &= Q(genre__iexact=genre)
        if availability_status:
            query &= Q(availability_status=(availability_status.lower() == 'true'))  
        books = Book.objects.filter(query)
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)
            distance_threshold_km = 50
            books = [
                book for book in books
                if self.calculate_distance(latitude, longitude, book.latitude, book.longitude) <= distance_threshold_km
            ]
        paginator = self.pagination_class()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)

    
    @action(detail=False, methods=['get'], url_path='all')
    def get_all_books_except_mine(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(username=request.user.username)
            queryset = Book.objects.exclude(owner=user_profile.uuid).order_by('-created_on')            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = BookSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = BookSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

