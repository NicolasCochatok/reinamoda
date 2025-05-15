from django.urls import path
from . import views

urlpatterns = [
    # Página principal del store con o sin filtros
    path('', views.store, name="store"),
    path('<str:material_slug>/', views.store, name="products_by_material"),
    path('<str:material_slug>/<slug:category_slug>/', views.store, name="products_by_material_category"),

    # Detalle de producto
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail"),

    # Listado solo por categoría (ruta vieja si querés mantenerla)
    path('category/<slug:category_slug>/', views.store, name="products_by_category"),

    # Búsqueda
    path('search/', views.search, name='search'),

    # Enviar reseña
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

    # Importar Excel
    path('importar-excel/', views.importar_excel, name='importar_excel'),

    # Obtener talles según categoría
    path('get-sizes/', views.get_sizes_by_category, name='get_sizes_by_category'),
]
