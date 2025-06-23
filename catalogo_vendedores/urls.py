from django.urls import path
from . import views, api_views

urlpatterns = [
    # Página HTML del catálogo para vendedores
    path('', views.index, name='catalogo-index'),

    # Endpoints de la API
    path('api/productos/', api_views.ProductoListView.as_view(), name='producto-lista'),
    path('api/productos/<str:codigo_unico>/', api_views.ProductoDetalleView.as_view(), name='producto-detalle'),

    # Registro de venta con asignación de vendedor si está logueado
    path('api/ventas/', views.registrar_venta, name='registrar-venta'),
]
