from rest_framework import serializers
from store.models import Product
from catalogo_vendedores.models import Venta


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)  # Devuelve URL completa si MEDIA_URL está bien

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'codigo_unico',
            'codigo_proveedor',
            'price',
            'stock',
            'image',
        ]


class VentaSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Venta
        fields = [
            'id',
            'producto',
            'cantidad',
            'cliente',
            'metodo_pago',
            'pagado',
            'precio_unitario',
            'fecha_venta',
            'vendedor',
        ]
        read_only_fields = ['fecha_venta']

    def validate(self, data):
        producto = data['producto']
        cantidad = data['cantidad']

        if producto.stock < cantidad:
            raise serializers.ValidationError("Stock insuficiente para esta venta.")

        return data
