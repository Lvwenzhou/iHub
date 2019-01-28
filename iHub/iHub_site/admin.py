from django.contrib import admin


# Register your models here.
from iHub_site.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'no', 'name', 'gender', 'major', 'avatar', 'mail', 'weChat_id', 'reg_time', 'credit')


admin.site.register(Users, UsersAdmin)
