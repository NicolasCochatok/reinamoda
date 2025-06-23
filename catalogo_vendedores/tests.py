from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase, override_settings
from category.models import Category
from store.models import Product


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class ProductoDetalleAPITest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name="Test", slug="test")
        self.product = Product.objects.create(
            product_name="Test Product",
            slug="test-product",
            description="desc",
            price=10,
            stock=5,
            category=self.category,
        )
        self.client = APIClient()

    def test_detalle_producto_por_pk(self):
        url = reverse("producto-detalle-cbv", kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.product.pk)
