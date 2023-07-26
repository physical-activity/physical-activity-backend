from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('first_name', 'last_name')
    ordering = ('email',)
    empty_value_display = '-empty-'


admin.site.register(CustomUser)
