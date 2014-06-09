# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'User.user_id'
        db.alter_column(u'analyzer_user', 'user_id', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'User.user_id'
        db.alter_column(u'analyzer_user', 'user_id', self.gf('django.db.models.fields.IntegerField')(max_length=3))

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
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['analyzer']