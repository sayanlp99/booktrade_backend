from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'owner', 'created_on')

admin.site.register(Book, BookAdmin)
