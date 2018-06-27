# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
import collections

class Readers(models.Model):
    reader_id = models.CharField(primary_key=True, max_length=10)
    description = models.CharField(max_length=255, blank=True)
    user_id = models.IntegerField(blank=False,db_column='user_id',)

    class Meta:
        managed = False
        db_table = 'readers'

class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    active = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'locations'

class Animals(models.Model):
    animal_id = models.AutoField(primary_key=True)
    species = models.CharField(max_length=255, blank=True)
    field_data = JSONField(blank=True,load_kwargs={'object_pairs_hook': collections.OrderedDict})
    class Meta:
        managed = False
        db_table = 'animals'

class Tags(models.Model):
    tag_id = models.CharField(primary_key=True, max_length=10)
    description = models.CharField(max_length=500, blank=True)
    class Meta:
        managed = False
        db_table = 'tags'

class TagReads(models.Model):
    tag_reads_id = models.AutoField(max_length=10,primary_key=True)
    reader_id = models.ForeignKey('Readers',on_delete=models.CASCADE,db_column='reader_id',)
    tag_id = models.ForeignKey('Tags',on_delete=models.CASCADE,db_column='tag_id',)
    user_id = models.IntegerField(blank=False,db_column='user_id')
    tag_read_time = models.DateTimeField()
    field_data = JSONField(blank=True,load_kwargs={'object_pairs_hook': collections.OrderedDict})
    public = models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'tag_reads'
        unique_together = (("tag_reads_id","reader_id", "tag_id", "tag_read_time"),)

class UploadLocation(models.Model):
    user_id = models.IntegerField(blank=False,db_column='user_id',)
    location_id = models.ForeignKey('Locations',on_delete=models.CASCADE,db_column='location_id',)
    class Meta:
        managed = False
        db_table = 'upload_location'
        unique_together = (("user_id","location_id"),)


class ReaderLocation(models.Model):
    reader_id = models.OneToOneField(Readers, on_delete=models.CASCADE, primary_key=True,db_column='reader_id',)
    location_id = models.ForeignKey('Locations',on_delete=models.CASCADE,db_column='location_id',)
    start_timestamp = models.DateTimeField(blank=True, null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'reader_location'

class TagOwner(models.Model):
    user_id = models.IntegerField(blank=False,db_column='user_id',)
    tag_id = models.OneToOneField('Tags',on_delete=models.CASCADE,primary_key=True,db_column='tag_id',)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tag_owner'

class AnimalHitReader(models.Model):
    reader_id = models.ForeignKey('Readers',on_delete=models.CASCADE,db_column='reader_id',)
    animal_id = models.ForeignKey('Animals',on_delete=models.CASCADE,db_column='animal_id',)
    tag_id = models.ForeignKey('Tags',on_delete=models.CASCADE,)
    class Meta:
        managed = False
        db_table = 'animal_hit_reader'
        unique_together = (("reader_id", "animal_id", "tag_id"),)

class TaggedAnimal(models.Model):
    tag_id = models.OneToOneField('Tags',on_delete=models.CASCADE,primary_key=True,db_column='tag_id',)
    animal_id = models.ForeignKey('Animals',on_delete=models.CASCADE,db_column='animal_id',)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    field_data = JSONField(blank=True,load_kwargs={'object_pairs_hook': collections.OrderedDict})
    class Meta:
        managed = False
        db_table = 'tagged_animal'
