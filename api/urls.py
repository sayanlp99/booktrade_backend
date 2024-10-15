from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet
from exchange_request.views import ExchangeRequestViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'books', BookViewSet)
router.register(r'exchange_request', ExchangeRequestViewSet, basename='exchange_requests')

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('', include(router.urls)),
]
