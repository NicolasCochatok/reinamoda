from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery, SizeOption
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProductGalleryInLine(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInLine]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')


@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
    list_display = ('categoria_aplicable', 'valor')
    list_filter = ('categoria_aplicable',)
    search_fields = ('valor',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
