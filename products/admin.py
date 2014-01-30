from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'digits',)
    readonly_fields = ('uuid', 'status', 'params', 'digits', 'material', 'email', 'compile_job_id', 'upload_job_id', 'email_job_id', 'shapeways_url', 'created', 'modified',)

admin.site.register(Order, OrderAdmin)
