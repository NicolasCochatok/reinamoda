from django.db import models
from store.models import Product
from accounts.models import Account

class Venta(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    cliente = models.CharField(max_length=100, blank=True, null=True)

    metodo_pago = models.CharField(
        max_length=50,
        choices=[
            ('efectivo', 'Efectivo'),
            ('mercado_pago', 'Mercado Pago'),
            ('tarjeta', 'Tarjeta de crédito'),
            ('pendiente', 'Pendiente de pago'),
        ],
        default='pendiente'
    )
    pagado = models.BooleanField(default=False)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)

    vendedor = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='ventas',
        null=True,
        blank=True
    )

    def total(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        # Solo descuenta stock al crear una nueva venta
        if self.pk is None:
            if self.producto.stock >= self.cantidad:
                self.producto.stock -= self.cantidad
                self.producto.save()
            else:
                raise ValueError("Stock insuficiente para esta venta")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.product_name} x {self.cantidad} - {self.metodo_pago}"
