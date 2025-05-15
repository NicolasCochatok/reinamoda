from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def get_image_url(self):
        """
        Retorna la URL segura de la imagen del producto o una imagen por defecto si no está cargada.
        """
        if self.product.image and hasattr(self.product.image, 'url'):
            return self.product.image.url
        return '/static/images/no-image.png'

    def __str__(self):
        return self.product.product_name
