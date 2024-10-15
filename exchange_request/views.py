from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from authentication.models import UserProfile
from books.models import Book
from .models import ExchangeRequest
from .serializers import ExchangeRequestSerializer, ExchangeRequestCreateSerializer
from django.utils.timezone import now
import time

class ExchangeRequestViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ExchangeRequest.objects.all()
    serializer_class = ExchangeRequestSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = ExchangeRequestCreateSerializer(data=request.data)
            if serializer.is_valid():
                user_profile = UserProfile.objects.get(username=request.user.username)
                serializer.save(initiator=user_profile.uuid, created_on=int(time.time()))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = request.data
            serializer = ExchangeRequestCreateSerializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def list(self, request, *args, **kwargs):
        try:
            exchange_requests = self.get_queryset()
            response_data = []
            for exchange_request in exchange_requests:
                initiator_profile = UserProfile.objects.get(uuid=exchange_request.initiator)
                acceptor_profile = UserProfile.objects.get(uuid=exchange_request.acceptor)
                initiator_book = Book.objects.get(book_id=exchange_request.initiator_book_id)
                acceptor_book = Book.objects.get(book_id=exchange_request.acceptor_book_id)
                response_data.append({
                    'exchange_id': exchange_request.exchange_id,
                    'initiator': exchange_request.initiator,
                    'acceptor': exchange_request.acceptor,
                    'initiator_name': initiator_profile.full_name,
                    'acceptor_name': acceptor_profile.full_name,
                    'initiator_book': exchange_request.initiator_book_id,
                    'acceptor_book': exchange_request.acceptor_book_id,
                    'initiator_book_title': initiator_book.title,
                    'acceptor_book_title': acceptor_book.title,
                    'created_on': exchange_request.created_on,
                    'delivery_method': exchange_request.delivery_method,
                    'exchange_duration': exchange_request.exchange_duration,
                    'request_status': exchange_request.request_status,
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist as e:
            return Response({'error': f'User not found: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist as e:
            return Response({'error': f'Book not found: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

