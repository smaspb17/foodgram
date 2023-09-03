from django.contrib import admin

from .models import Subscribe


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    fields = ('user', 'author',)
    list_display = ('id', 'user', 'author')
