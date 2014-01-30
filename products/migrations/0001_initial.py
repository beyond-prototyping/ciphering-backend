# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'products_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('params', self.gf('jsonfield.fields.JSONField')()),
            ('digits', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('material', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'products', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'products_order')


    models = {
        u'products.order': {
            'Meta': {'object_name': 'Order'},
            'digits': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'params': ('jsonfield.fields.JSONField', [], {}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['products']