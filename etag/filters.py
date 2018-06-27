__author__ = 'mstacy'
import django_filters

from models import *

class ReadersFilter(django_filters.FilterSet):
    reader_id = django_filters.CharFilter(lookup_type='iexact')
    description = django_filters.CharFilter(lookup_type='iexact')
    user = django_filters.NumberFilter()

    class Meta:
        model = Readers
        #fields = ['reader_id',]
        fields = ['reader_id','description', 'user']


class LocationsFilter(django_filters.FilterSet):
    location_id = django_filters.NumberFilter()
    name = django_filters.CharFilter(lookup_type='icontains')
    min_lat = django_filters.NumberFilter(name='latitude',lookup_type='gte')
    max_lat = django_filters.NumberFilter(name='latitude',lookup_type='lte')
    min_long = django_filters.NumberFilter(name='longitude',lookup_type='gte')
    max_long = django_filters.NumberFilter(name='longitude',lookup_type='lte')
    active = django_filters.BooleanFilter()
    
    class Meta:
        model = Locations
        fields = ['location_id','name', 'latitude','longitude','active',]


class AnimalsFilter(django_filters.FilterSet):
    animal_id = django_filters.NumberFilter()
    species = django_filters.CharFilter(lookup_type='icontains')
    
    class Meta:
        model = Animals
        fields = ['animal_id','species']


class TagsFilter(django_filters.FilterSet):
    tag_id = django_filters.CharFilter(lookup_type='iexact')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Tags
        fields = ['tag_id','description']


class TagReadsFilter(django_filters.FilterSet):
    reader_id = django_filters.CharFilter(lookup_type='icontains')
    tag_id = django_filters.CharFilter(lookup_type='icontains')
    tag_reads_id = django_filters.NumberFilter()
    #user = django_filters.NumberFilter()
    min_read_time = django_filters.DateTimeFilter(name='tag_read_time',lookup_type='gte')
    max_read_time = django_filters.DateTimeFilter(name='tag_read_time',lookup_type='lte')
    public = django_filters.BooleanFilter(lookup_type='exact')

    class Meta:
        model = TagReads
        fields = ['reader_id','tag_id','tag_reads_id','tag_read_time','public']


class UploadLocationFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter()
    location_id = django_filters.NumberFilter()

    class Meta:
        model = UploadLocation
        fields = ['user','location_id']


class ReaderLocationFilter(django_filters.FilterSet):
    reader_id = django_filters.CharFilter(lookup_type='icontains')
    location_id = django_filters.NumberFilter()
    min_start_timestamp = django_filters.DateTimeFilter(name='start_timestamp', lookup_type='gte')
    max_start_timestamp = django_filters.DateTimeFilter(name='start_timestamp', lookup_type='lte')
    min_end_timestamp = django_filters.DateTimeFilter(name='end_timestamp', lookup_type='gte')
    max_end_timestamp = django_filters.DateTimeFilter(name='end_timestamp', lookup_type='lte')

    class Meta:
        model = ReaderLocation
        fields = ['reader_id','location_id', 'start_timestamp','end_timestamp']


class TagOwnerFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter()
    tag_id = django_filters.CharFilter(lookup_type='iexact')
    min_start_time = django_filters.DateTimeFilter(name='start_time',lookup_type='gte')
    max_start_time = django_filters.DateTimeFilter(name='start_time',lookup_type='lte')
    min_end_time = django_filters.DateTimeFilter(name='end_time',lookup_type='gte')
    max_end_time = django_filters.DateTimeFilter(name='end_time',lookup_type='lte')
    
    class Meta:
        model = TagOwner
        fields = ['user','tag_id', 'start_time','end_time']


class AnimalHitReaderFilter(django_filters.FilterSet):
    reader_id = django_filters.CharFilter(lookup_type='icontains')
    animal_id = django_filters.NumberFilter()
    tag_id = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = AnimalHitReader
        fields = ['reader_id', 'animal_id','tag_id']


class TaggedAnimalFilter(django_filters.FilterSet):
    tag_id = django_filters.CharFilter(lookup_type='icontains')
    animal_id = django_filters.NumberFilter()
    min_start_time = django_filters.DateTimeFilter(name='start_time',lookup_type='gte')
    max_start_time = django_filters.DateTimeFilter(name='start_time',lookup_type='lte')
    min_end_time = django_filters.DateTimeFilter(name='end_time',lookup_type='gte')
    max_end_time = django_filters.DateTimeFilter(name='end_time',lookup_type='lte')
    
    class Meta:
        model = TaggedAnimal
        fields = ['animal_id','tag_id', 'start_time','end_time']
