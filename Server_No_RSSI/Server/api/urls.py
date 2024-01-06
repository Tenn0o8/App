from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .token_serializer import MyTokenObtainPairView


urlpatterns  = [
  path('',views.getAPIRoutes.as_view(),name='all_api'),
  # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('note/',views.Notes.as_view(),name='get_note'),
  path('location_list/',views.User_location_list.as_view()),
  path('device_list/',views.User_device_list.as_view()),
  path('location_define/',views.Location_Define.as_view(), name='location_define'),
  path('location_modify/<int:pk>/',views.Location_Modify.as_view(),name='location_modify'),
  path('location_info/<int:pk>/',views.Location_Info.as_view()),
  path('device_define/',views.Device_define.as_view()),
  path('device_info/<int:pk>/',views.Device_Info.as_view()),
  path('device_info/IMU/<int:pk>/',views.Device_Info_Adding.as_view()),
  path('device_info/RSSI/<int:pk>/',views.RSSI_Info_Adding.as_view()),

]
# còn phần delete location, device
# tạo một account khác và sử dụng location này -> đã xong -> Giờ làm sao để admin nhìn được hết 
# tạo thông tin device 

