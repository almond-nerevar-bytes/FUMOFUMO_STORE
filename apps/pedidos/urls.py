from django.urls import path
from . import views

app_name = 'pedidos'  

urlpatterns = [
    path('carrito/', views.carrito_ver, name='carrito_ver'),
    path('carrito/agregar/<int:id>/', views.carrito_agregar, name='carrito_agregar'),
    path('carrito/restar/<int:id>/', views.carrito_restar, name='carrito_restar'),
    path('carrito/eliminar/<int:id>/', views.carrito_eliminar, name='carrito_eliminar'),
    path('carrito/limpiar/', views.carrito_limpiar, name='carrito_limpiar'),
    path('checkout/', views.checkout_simulado, name='checkout'),
]