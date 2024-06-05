from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'auth_token', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'auth_token')
    list_filter = ('is_verified', 'created_at')
    ordering = ('created_at',)

admin.site.register(Profile, ProfileAdmin)
