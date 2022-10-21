from django.urls import path
from .views import retrieve_vps, create_vps, change_vps_status, get_vps
app_name = 'api'

urlpatterns = [
    path('create_vps/', create_vps, name='create_vps'),
    path('get_vps/<int:vps_id>', retrieve_vps, name='retrieve_vps'),
    path('get_vps/', get_vps, name='get_vps'),
    path('change_status/<int:vps_id>', change_vps_status, name='change_vps_status'),
]
