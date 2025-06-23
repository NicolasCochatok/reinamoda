from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import VentaSerializer


def index(request):
    return render(request, 'catalogo_vendedores/index.html')


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Podés cambiarlo a IsAuthenticated si querés obligar login
def registrar_venta(request):
    serializer = VentaSerializer(data=request.data)
    if serializer.is_valid():
        # Si el usuario está autenticado, lo asociamos como vendedor
        vendedor = request.user if request.user.is_authenticated else None
        serializer.save(vendedor=vendedor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
