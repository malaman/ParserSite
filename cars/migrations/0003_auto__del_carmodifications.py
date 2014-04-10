# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CarModifications'
        db.delete_table('cars_carmodifications')


    def backwards(self, orm):
        # Adding model 'CarModifications'
        db.create_table('cars_carmodifications', (
            ('car_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarModels'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cars', ['CarModifications'])


    models = {
        'cars.carmarks': {
            'Meta': {'object_name': 'CarMarks'},
            'auto_ria_id': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cars.carmodels': {
            'Meta': {'object_name': 'CarModels'},
            'car_mark': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.CarMarks']"}),
            'car_series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.CarSeries']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cars.carseries': {
            'Meta': {'object_name': 'CarSeries'},
            'car_mark': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.CarMarks']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'series_auto_ria_id': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['cars']