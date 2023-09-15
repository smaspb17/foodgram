from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Subscribe

UserModel = get_user_model()
admin.site.unregister(UserModel)


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    fields = ('user', 'author',)
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
