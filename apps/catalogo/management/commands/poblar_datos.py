from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.catalogo.models import Categoria, PelucheFumo


class Command(BaseCommand):
    help = "Pobla la base de datos con categorías y peluches Fumo de prueba."

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@fumoshop.cl", "admin")
            self.stdout.write(self.style.SUCCESS("✓ Superusuario 'admin' creado."))

        categorias = {
            "Touhou Project": "Peluches Fumo oficiales de la saga Touhou Project.",
            "Uma Musume": "Peluches Fumo y mascots de Uma Musume: Pretty Derby.",
        }
        cat_map = {}
        for nombre, desc in categorias.items():
            cat, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
            cat_map[nombre] = cat

        fumos = [
            ("Peluche Fumo Reimu Hakurei (Kourindou Ver.)", cat_map["Touhou Project"], "Gift", 74990, 5, True),
            ("Peluche Fumo Marisa Kirisame (V1)", cat_map["Touhou Project"], "Gift", 69990, 8, True),
            ("Peluche Fumo Special Week", cat_map["Uma Musume"], "Gift", 64990, 4, True),
            ("Peluche Fumo Tokai Teio", cat_map["Uma Musume"], "Gift", 64990, 6, True),
        ]
        for nom, cat, fab, pre, stk, dest in fumos:
            PelucheFumo.objects.get_or_create(nombre=nom, defaults={
                'categoria': cat, 'fabricante': fab, 'precio': pre, 'stock': stk, 'destacado': dest, 'activo': True
            })

        self.stdout.write(self.style.SUCCESS("✓ Catálogo Fumo poblado exitosamente."))