from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Fumo, Categoria  
from .forms import FumoForm         
# Create your views here.

def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def fumo_lista(request):  # Renombrado opcional o mantenido coherente
    query = request.GET.get('q', '').strip()
    categoria_slug = request.GET.get('categoria', '')
    orden = request.GET.get('orden', '-fecha_creacion')

    fumos = Fumo.objects.filter(activo=True).select_related('categoria')

    if categoria_slug:
        fumos = fumos.filter(categoria__slug=categoria_slug)

    if query:
        fumos = fumos.filter(
            Q(nombre__icontains=query) |
            Q(fabricante__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )

    ordenes_validos = {
        'precio_asc': 'precio',
        'precio_desc': '-precio',
        'nombre_asc': 'nombre',
        'recientes': '-fecha_creacion',
    }
    fumos = fumos.order_by(ordenes_validos.get(orden, '-fecha_creacion'))

    paginador = Paginator(fumos, 6)
    pagina = paginador.get_page(request.GET.get('page'))
    categorias = Categoria.objects.filter(activo=True)

    return render(request, 'catalogo/fumo_lista.html', {
        'figuras': pagina,  # Se mantiene la variable 'figuras' si tu HTML la usa así, o puedes cambiarla a 'fumos'
        'categorias': categorias,
        'categoria_seleccionada': categoria_slug,
        'query_actual': query,
        'orden_actual': orden,
        'total_resultados': fumos.count(),
    })


def fumo_detalle(request, slug):
    fumo = get_object_or_404(Fumo.objects.select_related('categoria'), slug=slug, activo=True)
    relacionadas = Fumo.objects.filter(categoria=fumo.categoria, activo=True).exclude(pk=fumo.pk)[:3]
    return render(request, 'catalogo/fumo_detalle.html', {'figura': fumo, 'relacionadas': relacionadas})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def gestion_fumos(request):
    query = request.GET.get('q', '').strip()
    fumos = Fumo.objects.all().select_related('categoria')
    if query:
        fumos = fumos.filter(Q(nombre__icontains=query) | Q(fabricante__icontains=query))
    paginador = Paginator(fumos.order_by('-fecha_creacion'), 10)
    pagina = paginador.get_page(request.GET.get('page'))
    return render(request, 'catalogo/gestion_fumos.html', {'figuras': pagina, 'query': query})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def fumo_crear(request):
    if request.method == 'POST':
        form = FumoForm(request.POST, request.FILES)
        if form.is_valid():
            fumo = form.save()
            messages.success(request, f"¡Peluche Fumo '{fumo.nombre}' registrado y agregado exitosamente!")
            return redirect('catalogo:gestion')
    else:
        form = FumoForm()
    return render(request, 'catalogo/fumo_form.html', {'form': form, 'titulo_accion': 'Ingresar Nuevo Peluche Fumo', 'boton_texto': 'Guardar Fumo'})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def fumo_editar(request, id):
    fumo = get_object_or_404(Fumo, id=id)
    if request.method == 'POST':
        form = FumoForm(request.POST, request.FILES, instance=fumo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Peluche Fumo '{fumo.nombre}' actualizado correctamente.")
            return redirect('catalogo:gestion')
    else:
        form = FumoForm(instance=fumo)
    return render(request, 'catalogo/fumo_form.html', {'form': form, 'figura': fumo, 'titulo_accion': 'Editar Peluche Fumo', 'boton_texto': 'Actualizar Fumo'})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def fumo_eliminar(request, id):
    fumo = get_object_or_404(Fumo, id=id)
    if request.method == 'POST':
        nombre = fumo.nombre
        fumo.delete()
        messages.success(request, f"Peluche Fumo '{nombre}' eliminado del sistema.")
        return redirect('catalogo:gestion')
    return render(request, 'catalogo/fumo_confirmar_eliminar.html', {'figura': fumo})