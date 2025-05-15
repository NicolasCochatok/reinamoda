from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    TIPO_TALLE_CHOICES = (
        ('anillo', 'Anillo'),
        ('pulsera', 'Pulsera'),
        ('collar', 'Collar'),
        ('aro', 'Aro'),
        ('dije', 'Dije'),
    )

    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    tipo_talle = models.CharField(max_length=20, choices=TIPO_TALLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

