from django.contrib import admin
from .models import UserProfile

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'company_name', 'email_verified', 'user_registered')

admin.site.register(UserProfile, UserAdmin)
