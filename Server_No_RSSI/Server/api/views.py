from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import NoteSerializer,DeviceSerializer,LocationSerializer,DeviceInfoSerializer,RSSIInfoSerializer
from .models import Note,Location_Schema,Device,Device_Info,RSSI_Info
from .publish import Condition_publish


class getAPIRoutes(APIView):

  def __init__(self):
    self.routes = [
      '/api/token/ for logging in',
      '/api/token/refresh/ for getting the refresh token',
      '/api/user_location/ for getting the location_id of current user',
      '/api/location_define/ for defining,deleting a new location',
      '/api/location/ for getting location information',
      '/api/location_modify/<int:pk>/ for updating the location',
      '/api/device_define/ for registing new device in a location',
      '/api/device/ for deleting device ',
      '/api/device_info/ for info, turning on/off',
      '/api/init_fire/ for fire localization, deleting the fire'
    ]

  def get(self,request,*args,**kwargs):
      return Response(self.routes)


class Notes(APIView):
   
  permission_classes = [IsAuthenticated]
  def get(self,request,*args,**kwargs):
      user = request.user
      if request.user.is_staff:
        notes = Note.objects.all()
      else:
        notes = user.note_set.all()
      serializer = NoteSerializer(notes,many=True)
      return Response(serializer.data)

class User_location_list(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,*args,**kwargs):
    try:
      user = request.user
      location_list = list(Location_Schema.objects.filter(user=user).values('pk','location_name'))
      if not location_list:
        return Response({"Message:""There is no location_shcema for this user"})
      else:
        return Response({"location_list":location_list})
    except:
      return Response("There is no location for this user")
    
class User_device_list(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,*args,**kwargs):
    try:
      user = request.user

      if 'location_id' in request.data:
        device_list = list(Device.objects.filter(user=user,location_schema=request.data['location_id']).values('pk','device_name'))
      else:
        device_list = list(Device.objects.filter(user=user).values('pk','device_name'))

      if not device_list:
        return Response({"Message:""There is no device for this user"})
      else:
        return Response({"device_list":device_list})
    except:
      return Response("There is no device for this user")

class Location_Define(APIView):
  permission_classes = [IsAuthenticated]
  def post(self,request,*args,**kwargs):
    user = request.user
    try:
      payload = {
        'user': user.id,
         'location_name': request.data['location_name'],
         'location_range': request.data['location_range'],
         'router_number': request.data['router_number'],
         'router_location': request.data['router_location'],
         'fire_location': request.data['fire_location'],
        }
      serializer = LocationSerializer(data=payload)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({
            'messages:' 'Successful'
         })
      
    except:
      return Response({
            'messages:' 'Check your data again',
      })

class Location_Modify(APIView):
  permission_classes = [IsAuthenticated]

  def get_location(self,request,pk):
    try:
      user = request.user
      return Location_Schema.objects.get(pk=pk,user=user)
    except:
      return Response({
        'messages:' 'Your location does not exist',
      })
    
  def put(self,request,pk):
    try:
      current_location = self.get_location(request,pk=pk)
      if 'location_name' in request.data:
        current_location.location_name = request.data['location_name']
      if 'fire_location' in request.data:
        current_location.fire_location = request.data['fire_location']
      if 'condition' in request.data:
        current_location.condition = request.data['condition']
      current_location.save()
      return Response({
        'messages:' 'Successful',
      })
    except:
      return Response({
        'messages:' 'Cannot update your location',
      })
    
  def delete(self,request,pk):
    try:
      current_location = self.get_location(request,pk=pk)
      current_location.delete()
      return Response({"message": "Object deleted successfully"})
    except:
      return Response({"message": "Object cannot be deleted"})


class Location_Info(APIView):
  permission_classes = [IsAuthenticated]
  def get_location(self,request,pk):
    try:
      user = request.user
      return Location_Schema.objects.get(pk=pk,user=user)
    except:
      return Response({
        'messages:' 'Your location does not exist',
      })

  def get(self,request,pk):
    try:
      current_location = self.get_location(request,pk=pk)
      serializer = LocationSerializer(instance=current_location,excluded_fields=['id','user'])
      return Response(serializer.data)
    
    except:
      return Response({
        'messages:' 'This location is not exist or you do not have permission',
      })

class Device_define(APIView):
  permission_classes=[IsAuthenticated]
  def post(self,request,*args,**kwargs):
    user = request.user
    try:

      # kiểm tra location_schema là của user
      location_schema_id = request.data['location_schema']
      try:
        location_schema = Location_Schema.objects.get(id=location_schema_id,user=user)
      except Location_Schema.DoesNotExist:
        return Response({
          "error": "Location_Schema does not exist or does not belong to the current user"})

      payload = {
        'user': user.id,
        'location_schema': request.data['location_schema'],
        'device_name': request.data['device_name'],
        }
      serializer = DeviceSerializer(data=payload)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({
            'messages:' 'Successful'
         })
      
    except:
      return Response({
            'messages:' 'Check your data again',
      })
    
class Device_Info(APIView):
  permission_classes = [IsAuthenticated]
  def get_device(self,request,pk):
    try:
      user = request.user
      return Device.objects.get(pk=pk,user=user)
    except:
      return Response({
        'messages:' 'Your device does not exist'
      })

  # lấy thông tin về thiết bị, cả RSSI và IMU 
  def get(self,request,pk):
    try:
      current_device = self.get_device(request,pk=pk)
      lastest_device_info = current_device.device_info_set.order_by('-date_created')[0]
      lastest_rssi_info = current_device.rssi_info_set.order_by('-date_created')[0]
      device_serializer = DeviceSerializer(instance=current_device,excluded_fields=['id','user'])
      device_info_serializer = DeviceInfoSerializer(instance=lastest_device_info,excluded_fields=['id','device'] )
      rssi_info_serializer = RSSIInfoSerializer(instance = lastest_rssi_info, excluded_fields = ['id','device'])

      if not device_info_serializer:
        payload = {**device_serializer.data,
                   "message": "There is no more information about this device"}
      else:
        payload = {**device_serializer.data,**device_info_serializer.data,**rssi_info_serializer.data}

      return Response(payload)
    except:
      return Response({
        'messages:' 'This device is not exist or you do not have permission'
      })
    
  # Thay đổi tên và tạng thái thiết bị
  def put(self,request,pk):
    try:
      current_device = self.get_device(request,pk=pk)
      # có thể update luôn tên của thiết bị
      if 'device_name' in request.data:
        current_device.device_name = request.data['device_name']
      if 'condition' in request.data:
        current_device.condition = request.data['condition']
        Condition_publish(request.data['condition'],pk)

      current_device.save()
      
      
      return Response({
        'messages:' 'Successful',
      })
    except:
      return Response({
        'messages:' 'Cannot update your device',
      })
    
    
  def delete(self,request,pk):
    try:
      current_device = self.get_device(request,pk=pk)
      current_device.delete()
      return Response({"message": "Object deleted successfully"})
    except:
      return Response({"message": "Object cannot be deleted"})
    
class Device_Info_Adding(APIView):
  permission_classes = [IsAuthenticated]
  def get_device(self,request,pk):
    try:
      user = request.user
      return Device.objects.get(pk=pk,user=user)
    except:
      return Response({
        'messages:' 'Your device does not exist'
      })
    
  # lấy thông tin về một list giá trị đo IMU
  def get(self,request,pk):
    try: 
      current_device = self.get_device(request,pk=pk)
      number = int(request.data['number'])
      lastest_device_info = current_device.device_info_set.order_by('-date_created')[:number]

      lastest_device_info_serializer = DeviceInfoSerializer(instance=lastest_device_info,excluded_fields=['id','device'],many=True)
      return Response(lastest_device_info_serializer.data)
  
    except:
      return Response({
        'messages:' 'Do not have enough data'
      })
    
  def put(self,request,pk):
    try: 
      payload = {
        'device': pk,
        'gyroR': request.data['gyroR'],
        'gyroP': request.data['gyroP'],
        'gyroY': request.data['gyroY'],
        'accX': request.data['accX'],
        'accY': request.data['accY'],
        'accZ': request.data['accZ'],
        'magX': request.data['magX'],
        'magY': request.data['magY'],
        'magZ': request.data['magZ'],
        'spinkler': request.data['spinkler'],
      }
      serializer = DeviceInfoSerializer(data=payload)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({
        'messages:' 'Successful'
      })

    except:
      return Response({
        'messages:' 'Cannot update your data'
      })

class RSSI_Info_Adding(APIView):
  permission_classes = [IsAuthenticated]
  def get_device(self,request,pk):
    try:
      user = request.user
      return Device.objects.get(pk=pk,user=user)
    except:
      return Response({
        'messages:' 'Your device does not exist'
      })
    
  # lấy thông tin về một list giá trị đo RSSI
  def get(self,request,pk):
    # try: 
      current_device = self.get_device(request,pk=pk)
      number = int(request.data['number'])
      lastest_rssi_info = current_device.rssi_info_set.order_by('-date_created')[:number]

      lastest_rssi_info_serializer = RSSIInfoSerializer(instance=lastest_rssi_info,excluded_fields=['id','device'],many=True)
      return Response(lastest_rssi_info_serializer.data)
    # except:
    #   return Response({
    #     'messages:' 'Do not have enough data'
    #   })
    
  def put(self,request,pk):
    # try: 
      current_device = self.get_device(request,pk=pk)
      new_rssi_data = RSSI_Info(device = current_device,rssi_list = request.data['rssi_list'])
      new_rssi_data.save()

      return Response({
        'messages:' 'Successful'
      })

      
    # except:
    #   return Response({
    #     'messages:' 'Cannot update your data'
    #   })