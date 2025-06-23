from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from .serializers import VentaSerializer, ProductSerializer
from store.models import Product
from django.db.models import Q


# 🖼️ Vista HTML del catálogo
def catalogo_productos(request):
    """Renderiza el catálogo para vendedores.

    Se puede filtrar mediante el parámetro ``q``. Solo se muestran productos
    disponibles con stock positivo para evitar errores al registrar ventas.
    """

    query = request.GET.get('q', '')
    productos = Product.objects.filter(is_available=True, stock__gt=0)
    if query:
        productos = productos.filter(Q(product_name__icontains=query))

    context = {
        'productos': productos
    }
    return render(request, 'catalogo_vendedores/index.html', context)


# ✅ API REST para traer productos con stock
@api_view(['GET'])
@permission_classes([AllowAny])
def lista_productos(request):
    query = request.GET.get('q', '')
    productos = Product.objects.filter(
        Q(product_name__icontains=query),
        stock__gt=0,
        is_available=True
    )
    serializer = ProductSerializer(productos, many=True, context={'request': request})
    return Response(serializer.data)


# ✅ API REST para registrar una venta
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_venta(request):
    serializer = VentaSerializer(data=request.data)
    if serializer.is_valid():
        vendedor = request.user if request.user.is_authenticated else None
        serializer.save(vendedor=vendedor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
