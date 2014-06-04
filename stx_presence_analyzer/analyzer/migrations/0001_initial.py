# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'analyzer_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('avatar', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'analyzer', ['User'])

        # Adding model 'Presence'
        db.create_table(u'analyzer_presence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analyzer.User'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'analyzer', ['Presence'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'analyzer_user')

        # Deleting model 'Presence'
        db.delete_table(u'analyzer_presence')


    models = {
        u'analyzer.presence': {
            'Meta': {'object_name': 'Presence'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analyzer.User']"})
        },
        u'analyzer.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['analyzer']