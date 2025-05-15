from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joinded', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joinded')
    ordering = ('-date_joinded',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture and object.profile_picture.name:
            return format_html(
                '<img src="{}" width="30" style="border-radius:50%;">',
                object.profile_picture.url
            )
        return "(Sin imagen)"

    thumbnail.short_description = "Imagen de perfil"
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


# Registro de modelos
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
