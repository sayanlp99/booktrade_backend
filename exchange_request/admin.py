from django.contrib import admin
from .models import ExchangeRequest

class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = ('exchange_id', 'delivery_method', 'request_status', 'created_on')

admin.site.register(ExchangeRequest, ExchangeRequestAdmin)
