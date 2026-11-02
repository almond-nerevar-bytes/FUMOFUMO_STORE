from uuid import uuid4

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.catalogo.models import PelucheFumo 

def _obtener_carrito(request):
    return request.session.setdefault('carrito', {})


def carrito_ver(request):
    carrito = _obtener_carrito(request)
    subtotal = sum(item['subtotal'] for item in carrito.values())
    iva = int(subtotal * 0.19)
    total = subtotal + iva
    return render(request, 'pedidos/carrito.html', {
        'items_carrito': carrito.values(),
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'esta_vacio': len(carrito) == 0,
    })


def carrito_agregar(request, id):
    fumo = get_object_or_404(PelucheFumo, id=id, activo=True)
    carrito = _obtener_carrito(request)
    str_id = str(fumo.id)

    cantidad_actual = carrito.get(str_id, {}).get('cantidad', 0)
    nueva_cantidad = cantidad_actual + 1

    if nueva_cantidad > fumo.stock:
        messages.warning(request, f"Límite de stock alcanzado ({fumo.stock} unidades) para el peluche Fumo '{fumo.nombre}'.")
        return redirect('pedidos:ver')

    imagen_url = fumo.imagen.url if fumo.imagen else ''
    carrito[str_id] = {
        'id': fumo.id,
        'nombre': fumo.nombre,
        'slug': fumo.slug,
        'fabricante': fumo.fabricante,
        'precio': int(fumo.precio),
        'cantidad': nueva_cantidad,
        'subtotal': int(fumo.precio) * nueva_cantidad,
        'imagen_url': imagen_url,
    }

    request.session.modified = True
    messages.success(request, f"¡Peluche Fumo '{fumo.nombre}' añadido al carrito de importación!")
    return redirect(request.META.get('HTTP_REFERER') or 'pedidos:ver')


def carrito_restar(request, id):
    carrito = _obtener_carrito(request)
    str_id = str(id)
    item = carrito.get(str_id)
    if item:
        if item['cantidad'] > 1:
            item['cantidad'] -= 1
            item['subtotal'] = item['precio'] * item['cantidad']
        else:
            del carrito[str_id]
        request.session.modified = True
    return redirect('pedidos:ver')


def carrito_eliminar(request, id):
    carrito = _obtener_carrito(request)
    if carrito.pop(str(id), None) is not None:
        request.session.modified = True
    return redirect('pedidos:ver')


def carrito_limpiar(request):
    _obtener_carrito(request).clear()
    request.session.modified = True
    return redirect('pedidos:ver')


@login_required
def checkout_simulado(request):
    carrito = _obtener_carrito(request)
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('pedidos:ver')

    items = [item.copy() for item in carrito.values()]
    subtotal = sum(item['subtotal'] for item in items)
    iva = int(subtotal * 0.19)
    total = subtotal + iva
    orden_id = uuid4().hex[:8].upper()

    carrito.clear()
    request.session.modified = True
    return render(request, 'pedidos/checkout_exito.html', {
        'items': items,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'orden_id': orden_id,
    })