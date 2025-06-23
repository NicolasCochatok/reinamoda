from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from store.models import Product
from .models import Venta
from .serializers import ProductSerializer, VentaSerializer


# 🔍 Listado de productos filtrado por texto y con stock disponible
class ProductoListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Product.objects.filter(
            (
                Q(product_name__icontains=query) |
                Q(codigo_proveedor__icontains=query) |
                Q(codigo_unico__icontains=query)
            ),
            stock__gt=0  # Solo mostrar si hay stock
        )


# 📦 Detalle de un producto individual por su ID
class ProductoDetalleView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# 💰 Registro de una venta con validación de stock
class RegistrarVentaView(generics.CreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
