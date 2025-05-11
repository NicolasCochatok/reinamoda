from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),

    # Primero va la URL más específica: detalle de producto
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail"),

    # Luego la URL de listado por categoría
    path('category/<slug:category_slug>/', views.store, name="products_by_category"),

    # Búsqueda
    path('search/', views.search, name='search'),

    # Enviar reseña
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

    # Importar Excel
    path('importar-excel/', views.importar_excel, name='importar_excel'),
]

