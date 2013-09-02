# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Widget'
        db.create_table(u'cms_widget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('create_version', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('modify_version', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'cms', ['Widget'])


    def backwards(self, orm):
        # Deleting model 'Widget'
        db.delete_table(u'cms_widget')


    models = {
        u'cms.widget': {
            'Meta': {'object_name': 'Widget'},
            'create_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'modify_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        }
    }

    complete_apps = ['cms']