from django.urls import path
from . import views, api_views

urlpatterns = [
    # Página HTML del catálogo
    path('', views.catalogo_productos, name='catalogo-index'),

    # APIs funcionales
    path('api/productos/', views.lista_productos, name='producto-lista-funcion'),
    path('api/ventas/', views.registrar_venta, name='registrar-venta'),

    # APIs con vistas basadas en clase
    path('api/cbv/productos/', api_views.ProductoListView.as_view(), name='producto-lista-cbv'),
    path('api/cbv/productos/<int:pk>/', api_views.ProductoDetalleView.as_view(), name='producto-detalle-cbv'),
]
