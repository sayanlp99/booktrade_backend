from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'books', BookViewSet)

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('', include(router.urls)),
]
