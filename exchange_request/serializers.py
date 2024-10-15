from rest_framework import serializers
from .models import ExchangeRequest

class ExchangeRequestSerializer(serializers.ModelSerializer):
    initiator_name = serializers.CharField(read_only=True)
    acceptor_name = serializers.CharField(read_only=True)
    initiator_book_title = serializers.CharField(read_only=True)
    acceptor_book_title = serializers.CharField(read_only=True)

    class Meta:
        model = ExchangeRequest
        fields = [
            'exchange_id', 
            'initiator', 
            'acceptor', 
            'initiator_name', 
            'acceptor_name', 
            'initiator_book', 
            'acceptor_book', 
            'initiator_book_title', 
            'acceptor_book_title', 
            'created_on', 
            'delivery_method', 
            'exchange_duration', 
            'request_status'
        ]

class ExchangeRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRequest
        fields = ['acceptor', 'initiator_book_id', 'acceptor_book_id', 'delivery_method', 'exchange_duration']
