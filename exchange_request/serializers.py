from rest_framework import serializers
from .models import ExchangeRequest

class ExchangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRequest
        fields = '__all__'

class ExchangeRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRequest
        fields = ['acceptor', 'initiator_book_id', 'acceptor_book_id', 'delivery_method', 'exchange_duration']
