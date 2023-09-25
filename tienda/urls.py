from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro-usuario'),
    path('login/', views.custom_login, name='login-usuario'),
    path('logout/', views.custom_logout, name='logout-usuario'),
    path('productos/', views.ListaProductosView, name='lista-productos'),
    path('pedidos/', views.ListaPedidosView, name='lista-pedidos'),
    path('hacerPedido/<int:pk>/', views.agregar_producto, name='hacer-pedido'),
    path('verPedido/<int:pk>/', views.verPedido, name='ver-pedido'),
    path('cambiarEstadoPedido/<int:pk>/', views.cambioEstadoPedido, name='cambiarEstadoPedido'),
    path('tomar_pedido/', views.tomar_pedido, name='tomar-pedidos')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)