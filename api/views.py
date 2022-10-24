from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Vps

from .serializers import VpsSerializer


@api_view(['GET'])
def retrieve_vps(request, vps_id):
    serialized_vps = VpsSerializer(get_object_or_404(Vps, id=vps_id)).data
    return Response({
        'vps': serialized_vps
    })


@api_view(['POST'])
def create_vps(request):
    if int(request.data.get('cpu_cores')) <=0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    vps = Vps.objects.create(cpu_cores=request.data.get('cpu_cores'), ram=request.data.get('ram'),
                             hdd=request.data.get('hdd'), status=request.data.get('status'))
    serialized_vps = VpsSerializer(vps).data
    return Response({
        'vps': serialized_vps
    })


@api_view(['GET'])
def get_vps(request):
    queryset = Vps.objects.filter(Q(cpu_cores=request.GET.get('cpu_cores')) | Q(ram=request.GET.get('ram')) |
                                  Q(hdd=request.GET.get('hdd')) | Q(status=request.GET.get('status')))
    serialized_vps = VpsSerializer(queryset, many=True).data
    if not serialized_vps:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({
        'vps': serialized_vps
    })


@api_view(['POST'])
def change_vps_status(request, vps_id):
    vps = get_object_or_404(Vps, id=vps_id)
    vps.status = request.data.get('status')
    vps.save()
    return Response({
        'vps': VpsSerializer(vps).data
    })
