# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CarMarks'
        db.create_table('cars_carmarks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('auto_ria_id', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('cars', ['CarMarks'])

        # Adding model 'CarSeries'
        db.create_table('cars_carseries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('car_mark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarMarks'])),
            ('series_auto_ria_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('cars', ['CarSeries'])

        # Adding model 'CarModels'
        db.create_table('cars_carmodels', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('car_mark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarMarks'])),
            ('car_series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarSeries'])),
        ))
        db.send_create_signal('cars', ['CarModels'])

        # Adding model 'CarModifications'
        db.create_table('cars_carmodifications', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('car_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarModels'])),
        ))
        db.send_create_signal('cars', ['CarModifications'])


    def backwards(self, orm):
        # Deleting model 'CarMarks'
        db.delete_table('cars_carmarks')

        # Deleting model 'CarSeries'
        db.delete_table('cars_carseries')

        # Deleting model 'CarModels'
        db.delete_table('cars_carmodels')

        # Deleting model 'CarModifications'
        db.delete_table('cars_carmodifications')


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
        'cars.carmodifications': {
            'Meta': {'object_name': 'CarModifications'},
            'car_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.CarModels']"}),
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