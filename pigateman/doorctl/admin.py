from django.contrib import admin

from .models import accessKey, Door


class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'notify', 'notify_email', 'use_limit', 'created', 'expires', 'internal_comment', 'uses')

class DoorAdmin(admin.ModelAdmin):
    list_display = ('name', 'gpio_port')

admin.site.register(accessKey, AccessKeyAdmin)
admin.site.register(Door, DoorAdmin)

admin.site.site_header = "PiGateMan Admin"
admin.site.site_title = "PiGateMan Admin Portal"
admin.site.index_title = "Welcome to PiGateMan Admin Portal"
