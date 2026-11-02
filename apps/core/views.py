from django.shortcuts import render
from apps.catalogo.models import PelucheFumo, Categoria


def inicio(request):
    """
    Portada de FumoShop Chile con peluches Fumo destacados, categorías principales
    y la magia de Touhou y Uma Musume / coleccionables.
    """
    destacadas = PelucheFumo.objects.filter(
        activo=True,
        destacado=True
    ).select_related('categoria')[:4]

    categorias = Categoria.objects.filter(activo=True)[:6]

    return render(request, 'core/index.html', {
        'destacadas': destacadas,
        'categorias': categorias,
        'total_figuras': PelucheFumo.objects.filter(activo=True).count(),
        'total_categorias': Categoria.objects.filter(activo=True).count(),
    })


def nosotros(request):
    """
    Información institucional sobre FumoShop Chile,
    garantía de peluches Fumo originales (Gift / (somewhat) AmiAmi), envíos a todo Chile y atención al coleccionista.
    """
    return render(request, 'core/nosotres.html')