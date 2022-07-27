from django.contrib import admin

from .models import Hit, ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    fields = ('target', 'key')
    list_display = ('key', 'target', 'added', 'ttl')
    list_editable = ('ttl',)
    ordering = ('-added',)
    list_filter = ('added',)
    date_hierarchy = 'added'


@admin.register(Hit)
class HitAdmin(admin.ModelAdmin):
    list_display = ('target', 'ip', 'user_agent', 'referer', 'time')
    ordering = ('-time',)
    list_filter = ('target', 'referer', 'time')
    date_hierarchy = 'time'
