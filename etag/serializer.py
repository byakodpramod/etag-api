from rest_framework import serializers
import json
from models import *
import os, requests

class WritableJSONField(serializers.WritableField):
    def to_native(self, obj):
        return obj #json.dumps(obj)
    def from_native(self,value):
    return value #json.loads(value)

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value

class AnimalsSerializer(serializers.HyperlinkedModelSerializer):
    field_data=WritableJSONField()
    animal_id = serializers.CharField(source='animal_id')
    class Meta:
        model = Animals
        fields = ('url','animal_id','species','field_data')

class ReaderSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.Field(source='user_id')
    class Meta:
        model = Readers
        fields = ('url','reader_id','description','user_id')

class LocationsSerializer(serializers.HyperlinkedModelSerializer):
    location_id = serializers.CharField(source='location_id')
    class Meta:
        model = Locations
        fields = ('url','location_id','name','latitude','longitude','active')

class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ('url','tag_id','description',)

class ReaderLocationSerializer(serializers.HyperlinkedModelSerializer):
    reader_id = serializers.SlugRelatedField(slug_field='reader_id')
    location_id = serializers.SlugRelatedField(slug_field='location_id')
    class Meta:
        model = ReaderLocation
        fields = ('url','reader_id','location_id','start_timestamp','end_timestamp',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class TaggedAnimalSerializer(serializers.HyperlinkedModelSerializer):
    tag_id = serializers.SlugRelatedField(slug_field='tag_id')
    field_data=WritableJSONField() #serializers.DictField()
    animal_id = serializers.SlugRelatedField(slug_field='animal_id')
    class Meta:
        model = TaggedAnimal
        fields = ('url','tag_id','animal_id','start_time','end_time','field_data',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)
	 
class TagOwnerSerializer(serializers.HyperlinkedModelSerializer):
    tag_id = serializers.SlugRelatedField(slug_field='tag_id')
    user_id = serializers.Field(source='user_id')
    class Meta:
        model = TagOwner
        fields = ('url','tag_id','start_time','end_time','user_id',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class TagReadsSerializer(serializers.HyperlinkedModelSerializer):
    reader_id = serializers.SlugRelatedField(slug_field='reader_id')
    reader_url = serializers.HyperlinkedIdentityField(view_name='readers-detail')
    tag_id = serializers.SlugRelatedField(slug_field='tag_id')
    tag_url = serializers.HyperlinkedIdentityField(view_name='tags-detail')
    field_data = WritableJSONField()
    user_id = serializers.Field(source='user_id')

    class Meta:
        model = TagReads
        fields = ('url','reader_id','tag_id','field_data','tag_read_time','public','user_id')
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class AnimalHitReaderSerializer(serializers.HyperlinkedModelSerializer):
    reader_id = serializers.SlugRelatedField(slug_field='reader_id')
    tag_id = serializers.SlugRelatedField(slug_field='tag_id')
    animal_id = serializers.SlugRelatedField(slug_field='animal_id')
    class Meta:
        model = AnimalHitReader
        fields = ('url','reader_id','tag_id','animal_id')

class UploadLocationSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.Field(source='user_id')
    location_id = serializers.SlugRelatedField(slug_field='location_id')
    class Meta:
        model = UploadLocation
        fields = ('url','location_id','user_id')
