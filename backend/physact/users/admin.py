from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname')
    list_filter = ('email', 'name')


admin.site.unregister(Group)
