# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Order.shapeways_url'
        db.add_column(u'products_order', 'shapeways_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Order.compile_job_id'
        db.add_column(u'products_order', 'compile_job_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)

        # Adding field 'Order.upload_job_id'
        db.add_column(u'products_order', 'upload_job_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)

        # Adding field 'Order.email_job_id'
        db.add_column(u'products_order', 'email_job_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Order.shapeways_url'
        db.delete_column(u'products_order', 'shapeways_url')

        # Deleting field 'Order.compile_job_id'
        db.delete_column(u'products_order', 'compile_job_id')

        # Deleting field 'Order.upload_job_id'
        db.delete_column(u'products_order', 'upload_job_id')

        # Deleting field 'Order.email_job_id'
        db.delete_column(u'products_order', 'email_job_id')


    models = {
        u'products.order': {
            'Meta': {'object_name': 'Order'},
            'compile_job_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'digits': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_job_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'params': ('jsonfield.fields.JSONField', [], {}),
            'shapeways_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'upload_job_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['products']