from django.contrib import admin
from .models import Categoria, PelucheFumo

admin.site.site_header = "FumoShop Chile - Panel de Administración FUMOFUMO"
admin.site.site_title = "FumoShop Admin"
admin.site.index_title = "Gestión del Catálogo e Inventario de Peluches Fumo"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activo', 'creado_en')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ('activo',)


@admin.register(PelucheFumo)
class PelucheFumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fabricante', 'precio_formateado', 'stock', 'activo', 'destacado')
    list_filter = ('categoria', 'fabricante', 'activo', 'destacado')
    search_fields = ('nombre', 'fabricante', 'descripcion')
    list_editable = ('stock', 'activo', 'destacado')
    prepopulated_fields = {'slug': ('nombre',)}
    list_per_page = 15