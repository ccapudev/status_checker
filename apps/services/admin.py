from django.contrib import admin
from . import models


@admin.register(models.WebService)
class WebServiceAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'minutes', 'is_active', 'last_check'
    )


@admin.register(models.Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'status_code', 'reason', 'content_type', 'response_time'
    )
    readonly_fields = ('date_request',)


@admin.register(models.CheckpointErrors)
class CheckpointErrorsAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'reason'
    )
    readonly_fields = ('date_request',)
