from django.urls import path
from . import views

urlpatterns = [
    # 🔒 Rutas específicas (deben ir primero)
    path('importar-excel/', views.importar_excel, name='importar_excel'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('get-sizes/', views.get_sizes_by_category, name='get_sizes_by_category'),

    # 🛍️ Detalle de producto y categorías
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail"),
    path('category/<slug:category_slug>/', views.store, name="products_by_category"),

    # 🧩 Vistas dinámicas (van al final para no pisar otras)
    path('<str:material_slug>/<slug:category_slug>/', views.store, name="products_by_material_category"),
    path('<str:material_slug>/', views.store, name="products_by_material"),
    path('', views.store, name="store"),
]
