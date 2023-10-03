from django.contrib import admin
from user_management.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'profile_picture', 'user_id', 'date_of_birth']


admin.site.register(User, UserAdmin)

