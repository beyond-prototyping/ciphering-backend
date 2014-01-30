# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Order.created'
        db.add_column(u'products_order', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Order.modified'
        db.add_column(u'products_order', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 30, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Order.created'
        db.delete_column(u'products_order', 'created')

        # Deleting field 'Order.modified'
        db.delete_column(u'products_order', 'modified')


    models = {
        u'products.order': {
            'Meta': {'object_name': 'Order'},
            'compile_job_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'digits': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_job_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'params': ('jsonfield.fields.JSONField', [], {}),
            'shapeways_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'upload_job_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['products']