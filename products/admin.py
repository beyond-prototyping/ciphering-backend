from cStringIO import StringIO
from django.http import HttpResponse
from django.contrib import admin
import unicodecsv
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'digits', 'email', 'status', 'created', 'shapeways_link', )
    readonly_fields = ('uuid', 'status', 'params', 'digits', 'material', 'email', 'compile_job_id', 'upload_job_id', 'email_job_id', 'shapeways_url', 'created', 'modified',)
    actions = ['export_csv']

    def shapeways_link(self, instance):
        return u'<a href="{0}">{0}</a>'.format(instance.shapeways_url)
    shapeways_link.short_description = 'Shapeways Link'
    shapeways_link.allow_tags = True

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=ciphering-orders.csv'
        writer = unicodecsv.writer(response, encoding='utf-8')

        # header
        writer.writerow([field.name for field in queryset.model._meta.fields])

        # rows
        for row in queryset:
            writer.writerow([getattr(row, field.name) for field in queryset.model._meta.fields])

        return response
    export_csv.short_description = "Export selected orders in CSV format"


admin.site.register(Order, OrderAdmin)
