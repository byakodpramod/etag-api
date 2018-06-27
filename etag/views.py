from django.shortcuts import render
from rest_framework.authtoken.models import Token
#from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.renderers import BrowsableAPIRenderer, JSONPRenderer,JSONRenderer,XMLRenderer,YAMLRenderer #, filters
from .renderer import eventdropsJSONRenderer
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser,FileUploadParser
#from renderer import CustomBrowsableAPIRenderer
from filters import *
from etag.models import *
from serializer import *
#from serializer import AnimalsSerializer,ReaderSerializer,TaggedAnimalSerializer,ReaderLocationSerializer,TagOwnerSerializer,TagReadsSerializer,TagsSerializer,LocationsSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import os, requests,json
#import DjangoModelPermissionsOrAnonReadOnly


class ReadersViewSet(viewsets.ModelViewSet):
    """
    RFID Readers table view set.
    """
    model = Readers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ReaderSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ReadersFilter
    search_fields = ('user', 'description',)
    ordering_fields = '__all__'
    
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
        	return Readers.objects.filter(user_id=user.id)
        public_tag_readers = TagReads.objects.filter(public=True).values_list('reader_id')
	return Readers.objects.filter(reader_id__in=public_tag_readers)

    def pre_save(self, obj):
        obj.user_id = self.request.user.id

class AnimalsViewSet(viewsets.ModelViewSet):
    """
    RFID Animal table view set.
    """
    model = Animals
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AnimalsSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = AnimalsFilter
    #search_fields = ('user', 'description',)
    ordering_fields = '__all__'
    
    #def get_queryset(self):
    #    user = self.request.user
    #    if self.request.user.is_authenticated():
    #            if not user:
    #                    return []
    #            return Readers.objects.filter(user_id=user.id)
    #    public_tag_readers = TagReads.objects.filter(public=True).values_list('reader_id')
    #    return Readers.objects.filter(reader_id__in=public_tag_readers)

    #def pre_save(self, obj):
    #    obj.user_id = self.request.user.id

class LocationsViewSet(viewsets.ModelViewSet):
    """
    RFID Locations table view set.
    """
    model = Locations
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = LocationsSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = LocationsFilter
    #search_fields = ('user', 'description',)
    ordering_fields = '__all__'

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated():
                if not user:
                        return []
		private_reader_loc = ReaderLocation.objects.filter(reader_id__user_id=user.id).values_list('location_id').distinct()
                return Locations.objects.filter(location_id__in=private_reader_loc)
	public_reader_ids = TagReads.objects.filter(public=True).values_list('reader_id').distinct()
        public_reader_loc = ReaderLocation.objects.filter(reader_id__in=public_reader_ids).values_list('location_id').distinct()
        return Locations.objects.filter(location_id__in=public_reader_loc)

    #def pre_save(self, obj):
    #    obj.user_id = self.request.user.id

class ReaderLocationViewSet(viewsets.ModelViewSet):
    """
    Reader Location table view set.
    """
    model = ReaderLocation
    queryset = ReaderLocation.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ReaderLocationSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ReaderLocationFilter
    search_fields = ('start_timestamp','end_timestamp')
    ordering_fields = '__all__'
	
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
           		return []
		return ReaderLocation.objects.filter(reader_id__user_id=user.id)
	public_tag_readers = TagReads.objects.filter(public=True).values_list('reader_id')
	return ReaderLocation.objects.filter(reader_id__in=public_tag_readers)

	
class TaggedAnimalViewSet(viewsets.ModelViewSet):
    """
    Tagged Animal table view set.
    """
    model = TaggedAnimal
    queryset = TaggedAnimal.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TaggedAnimalSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = TaggedAnimalFilter
    ordering_fields = '__all__'
	
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
		private_tags = TagReads.objects.filter(public=False,user_id=user.id).values_list('tag_id').distinct()
        	return TaggedAnimal.objects.filter(tag_id__in=private_tags)
	public_tags = TagReads.objects.filter(public=True).values_list('tag_id').distinct()
        return TaggedAnimal.objects.filter(tag_id__in=public_tags)

class TagsViewSet(viewsets.ModelViewSet):
    """
    Tag Owner table view set.
    """
    model = Tags
    queryset = Tags.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagOwnerSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter ,filters.OrderingFilter)
    filter_class = TagsFilter
    #search_fields = ('tag_id',)
    ordering_fields = '__all__'
    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated():
                if not user:
                        return []
                user_tags = TagOwner.objects.filter(user_id=user.id).values_list('tag_id').distinct()
                return Tags.objects.filter(tag_id__in=user_tags)
        public_tags = TagReads.objects.filter(public=True).values_list('tag_id').distinct()
        return Tags.objects.filter(tag_id__in=public_tags)
	
class TagOwnerViewSet(viewsets.ModelViewSet):
    """
    TagOwner table view set.
    """
    model = TagOwner
    queryset = TagOwner.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagOwnerSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter ,filters.OrderingFilter)
    filter_class = TagOwnerFilter
    #search_fields = ('tag_id',)
    ordering_fields = '__all__'
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
        	return TagOwner.objects.filter(user_id=user.id)
	public_tags = TagReads.objects.filter(public=True).values_list('tag_id').distinct()
	return TagOwner.objects.filter(tag_id__in=public_tags)
    
    def pre_save(self, obj):
        obj.user_id = self.request.user.id
 
class TagReadsViewSet(viewsets.ModelViewSet):
    """
    TagReads table view set.
    """
    model = TagReads
    queryset = TagReads.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagReadsSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = TagReadsFilter
    search_fields = ('tag_id')
    ordering_fields = '__all__'
	
    def get_queryset(self):
	user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
		else :             
        		return TagReads.objects.filter(user_id = user.id)
	return TagReads.objects.filter(public=True)

    def pre_save(self, obj):
        obj.user_id = self.request.user.id

class AnimalHitReaderViewSet(viewsets.ModelViewSet):
    """
    RFID AnimalHitReader table view set.
    """
    model = AnimalHitReader
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AnimalHitReaderSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = AnimalHitReaderFilter
    #search_fields = ('user', 'description',)
    ordering_fields = '__all__'


class UploadLocationViewSet(viewsets.ModelViewSet):
    """
    RFID UploadLocation table view set.
    """
    model = UploadLocation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = UploadLocationSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = UploadLocationFilter
    #search_fields = ('user', 'description',)
    ordering_fields = '__all__'

    def pre_save(self, obj):
        obj.user_id = self.request.user.id

class etagDataUploadView(APIView):
        permission_classes =(IsAuthenticated,)
        #parser_classes = (MultiPartParser, FormParser,FileUploadParser,)
        parser_classes = (FileUploadParser,)
        renderer_classes = (JSONRenderer,)

        def post(self, request, uploadDirectory="/data/file_upload",format=None):
                #Get Token for task submission
                tok = Token.objects.get_or_create(user=self.request.user)
                headers = {'Authorization':'Token {0}'.format(str(tok[0])),'Content-Type':'application/json'} 
                #check if uploadDirectory exists
                if not os.path.isdir(uploadDirectory):
                    os.makedirs(uploadDirectory)
                result={} #'var':dir(request),'fpath':request.build_absolute_uri().split('/')}
                local_file=""
                reader_id = request.DATA.get("reader_id")
                public_id=  request.DATA.get("myCheck")
                if public_id != '1':
					public_id=False
                if public_id == '1':
					public_id=True
                #result={"reader_id":reader_id,"public_id":public_id}
                #return Response(result)
                for key,value in request.FILES.iteritems():
                        filename= value.name
                        local_file = "%s/%s" % (uploadDirectory,filename)
                        self.handle_file_upload(request.FILES[key],local_file)
                        result[key]=local_file
                #Request task
                task_name = "etagq.tasks.tasks.etagDataUpload"
                payload={"function": task_name,"queue": "celery","args":[reader_id,local_file,str(tok[0]),public_id],"kwargs":{},"tags":[]}
                components = request.build_absolute_uri().split('/')
                hostname = os.environ.get("host_hostname", components[2])
                r=requests.post("{0}//{1}/api/queue/run/etagq.tasks.tasks.etagDataUpload/.json".format(components[0],hostname),data=json.dumps(payload),headers=headers)
                return Response(r.json())


        def handle_file_upload(self,f,filename):
                if f.multiple_chunks():
                        with open(filename, 'wb+') as temp_file:
                                for chunk in f.chunks():
                                        temp_file.write(chunk)
                else:
                        with open(filename, 'wb+') as temp_file:
                                temp_file.write(f.read())
