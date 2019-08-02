from django.contrib import admin
from . import models


@admin.register(models.WebService)
class WebServiceAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'minutes', 'is_active', 'last_check'
    )
    list_editable = ['minutes', 'is_active']


@admin.register(models.Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'status_code', 'reason', 'content_type',
        'response_time', 'date_request'
    )
    readonly_fields = ('date_request',)
    list_filter = ['web_service__domain']
    


@admin.register(models.CheckpointErrors)
class CheckpointErrorsAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'reason', 'date_request'
    )
    readonly_fields = ('date_request',)
    list_filter = ['web_service__domain']
