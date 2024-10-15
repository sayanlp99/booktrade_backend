from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Book
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from authentication.models import UserProfile
from django.db.models import Q

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(username=request.user.username)
            queryset = Book.objects.filter(owner=user_profile.uuid)
            serializer = BookSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            print(request.data)
            serializer = BookSaveSerializer(data=request.data)
            if serializer.is_valid():
                user_profile = UserProfile.objects.get(username=request.user.username)
                serializer.save(owner=user_profile.uuid)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
        
    
    def get_books_by_user(self, request):
        try:
            user_id = request.query_params.get('userId')
            if not user_id:
                return Response({"error": "userId parameter is required"}, status=status.HTTP_400_BAD_REQUEST)        
            books = Book.objects.filter(owner=user_id)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def search_books(self, request):
        keyword = request.query_params.get('q')
        if not keyword:
            return Response({"error": "Search keyword 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)
        books = Book.objects.filter(
            Q(title__icontains=keyword) | 
            Q(author__icontains=keyword) | 
            Q(genre__icontains=keyword)
        )
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
