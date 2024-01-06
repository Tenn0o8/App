from rest_framework.serializers import ModelSerializer
from .models import Note, Location_Schema,Device,Device_Info,RSSI_Info

class NoteSerializer(ModelSerializer):
  class Meta:
    model = Note
    fields = '__all__'

class LocationSerializer(ModelSerializer):
  def __init__(self,*args,**kwargs):
    excluded_fields = kwargs.pop('excluded_fields',None)
    super(LocationSerializer, self).__init__(*args, **kwargs)
    # Exclude specified fields
    if excluded_fields:
      for field in excluded_fields:
        #self.fields là nơi chứa những field được serialize
        self.fields.pop(field, None)

  class Meta:
    model = Location_Schema
    fields = '__all__' 


class DeviceSerializer(ModelSerializer):
  class Meta:
    model = Device
    fields = '__all__' 

  def __init__(self,*args,**kwargs):
    excluded_fields = kwargs.pop('excluded_fields',None)
    super(DeviceSerializer, self).__init__(*args, **kwargs)
    # Exclude specified fields
    if excluded_fields:
      for field in excluded_fields:
        #self.fields là nơi chứa những field được serialize
        self.fields.pop(field, None)


class DeviceInfoSerializer(ModelSerializer):
  class Meta:
    model = Device_Info
    fields = '__all__' 

  def __init__(self,*args,**kwargs):
    excluded_fields = kwargs.pop('excluded_fields',None)
    super(DeviceInfoSerializer, self).__init__(*args, **kwargs)
    # Exclude specified fields
    if excluded_fields:
      for field in excluded_fields:
        #self.fields là nơi chứa những field được serialize
        self.fields.pop(field, None)

class RSSIInfoSerializer(ModelSerializer):
  class Meta:
    model = RSSI_Info
    fields = '__all__' 

  def __init__(self,*args,**kwargs):
    excluded_fields = kwargs.pop('excluded_fields',None)
    super(RSSIInfoSerializer, self).__init__(*args, **kwargs)
    # Exclude specified fields
    if excluded_fields:
      for field in excluded_fields:
        #self.fields là nơi chứa những field được serialize
        self.fields.pop(field, None)