from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json

# Create your models here.

class Note(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  body = models.TextField()
  def __str__(self):
    return f"{self.body}"
  # class Meta:
    # verbose_name = ""
    # verbose_name_plural = "Custom Name for Plural"


class Location_Schema(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  location_name = models.CharField(max_length=255)
  location_range = models.IntegerField()
  router_number = models.IntegerField()

  # chuyển từ text, json sang list
  router_location = models.TextField(max_length=255) #list chứa vị trí các router dạng text
  fire_location = models.TextField(max_length=255,default="[]") #list chứa vị trí các fire dạng text

  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  condition = models.BooleanField(default=True)

  def router_location_validation(self):
    try:
      value = self.get_router_location()
      if not len(value) == self.router_number:
        raise ValidationError('Length')
      for position in value:
        if not (0<=position<self.location_range):
          raise ValidationError('Router location')
      return True
    except ValidationError as va:
      if "Length" in str(va):
        raise ValidationError('Length of value must match router_number')
      if "Router location" in str(va):
        raise ValidationError('Router location must be in location_range')
    except:
      raise ValidationError("Wrong type of list for router")
    
  def fire_location_validation(self):
    try:
      value = self.get_fire_location()
      if len(value) == 0:
        return True
      for position in value:
        if not (0<=position<self.location_range):
          raise ValidationError('location_range')
      return True
    except ValidationError as va:
      if "location_range" in str(va):
          raise ValidationError('Fire location must be in location_range')
    except:
      raise ValidationError("Wrong type of list for fire")

  def set_router_location(self,value):
    if  len(value) == self.router_number:
      self.router_location = json.dumps(value)
    else:
      raise ValidationError('Length of value must match router_number')

  def get_router_location(self):
    return json.loads(self.router_location) if self.router_location else []
  
  def set_fire_location(self,value):

    result = True
    for position in value:
      if not (0<=position<self.location_range):
        result = False

    if result:
      self.fire_location = json.dumps(value)
    else: 
      raise ValidationError('Fire location must be in location_range')

  def get_fire_location(self):
    return json.loads(self.fire_location) if self.fire_location else []
  

  def __str__(self):
    return f"{self.location_name} --- ID: {self.id}"
  
  def save(self,*args,**kwargs):
    self.router_location_validation()
    self.fire_location_validation()
    super().save(*args,**kwargs)
  
class Device(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  location_schema = models.ForeignKey(Location_Schema,on_delete=models.CASCADE) 
  device_name = models.CharField(max_length=255)
  condition = models.BooleanField(default=True)

  
  def __str__(self):
    return f"{self.device_name} --- ID: {self.id}"


class Device_Info(models.Model):
  device = models.ForeignKey(Device, on_delete=models.CASCADE)
  date_created = models.DateTimeField(auto_now_add=True)
  gyroR = models.FloatField(default=0)
  gyroP = models.FloatField(default=0)
  gyroY = models.FloatField(default=0)
  accX = models.FloatField(default=0)
  accY = models.FloatField(default=0)
  accZ = models.FloatField(default=0)
  magX = models.FloatField(default=0)
  magY = models.FloatField(default=0)
  magZ = models.FloatField(default=0)
  spinkler = models.FloatField(default=0)

  def __str__(self):
    return f"IMU: {self.device.device_name} --- TimeStamp: {self.date_created} --- ID: {self.id}"

class RSSI_Info(models.Model):
  device = models.ForeignKey(Device, on_delete=models.CASCADE)
  device_location = models.IntegerField(default=-1) # phải nằm trong location_shema_range hoặc -1 nếu chưa biết
  rssi_list = models.TextField(max_length=255,default='[]') # chiều dài list bằng số lượng router
  date_created = models.DateTimeField(auto_now_add=True)


  def __str__(self):
    return f"RSSI: {self.device.device_name} --- ID: {self.id} --- TimeStamp: {self.date_created}"
  
  def get_rssi_list(self):
    return json.loads(self.rssi_list) if self.rssi_list else []
  
  def set_rssi_list(self,value): # must save later
    if len(value) == self.device.location_schema.router_number:
      self.rssi_list = json.dumps(value)
    else:
      raise ValidationError('Length of list must match router_number')
    
  def rssi_validation(self):
    try:
      value = self.get_rssi_list()
      # nếu list rỗng
      if not value:
        return True

      # chiều dài list phải đúng bằng số lượng router
      if not len(value) == self.device.location_schema.router_number:
        raise ValidationError('router_number')
      return True
    
    except ValidationError as va:
      if "router_number" in str(va):
          raise ValidationError('Length of list must match router_number')
    except:
      raise ValidationError("Length of list")
    

  def device_location_validation(self):
    value = self.device_location
    if value == -1:
      return True
    if not (0<=value<self.device.location_schema.location_range):
      raise ValidationError('Device location must be in location_range')
    return True
  
  def save(self,*args,**kwargs):
    self.device_location_validation()
    self.rssi_validation()
    super().save(*args,**kwargs)