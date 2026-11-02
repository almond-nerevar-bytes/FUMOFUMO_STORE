from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.fumo_lista, name='lista'),
    path('fumo/<slug:slug>/', views.fumo_detalle, name='detalle'),
    path('gestion/', views.gestion_fumos, name='gestion'),
    path('gestion/nuevo/', views.fumo_crear, name='crear'),
    path('gestion/editar/<int:id>/', views.fumo_editar, name='editar'),
    path('gestion/eliminar/<int:id>/', views.fumo_eliminar, name='eliminar'),
]