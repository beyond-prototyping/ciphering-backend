from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'digits', 'email', 'status', 'created', 'shapeways_link', )
    readonly_fields = ('uuid', 'status', 'params', 'digits', 'material', 'email', 'compile_job_id', 'upload_job_id', 'email_job_id', 'shapeways_url', 'created', 'modified',)

    def shapeways_link(self, instance):
        return u'<a href="{0}">{0}</a>'.format(instance.shapeways_url)
    shapeways_link.short_description = 'Shapeways Link'
    shapeways_link.allow_tags = True

admin.site.register(Order, OrderAdmin)
