from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Categoria, PelucheFumo


class CatalogPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username='catalog_admin',
            password='test-password',
            is_staff=True,
        )
        cls.category = Categoria.objects.create(nombre='Touhou Project')
        cls.fumo = PelucheFumo.objects.create(
            nombre='Reimu Hakurei',
            categoria=cls.category,
            descripcion='Peluche de prueba.',
            precio=74990,
            stock=2,
            destacado=True,
        )

    def test_public_pages_render_catalog_and_cart_links(self):
        home = self.client.get(reverse('core:inicio'))
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, '1 disponibles')
        self.assertContains(home, reverse('pedidos:ver'))

        about = self.client.get(reverse('core:nosotros'))
        self.assertEqual(about.status_code, 200)

        catalog = self.client.get(reverse('catalogo:lista'))
        self.assertEqual(catalog.status_code, 200)
        self.assertContains(catalog, self.fumo.nombre)
        self.assertContains(catalog, reverse('pedidos:agregar', args=[self.fumo.pk]))

        detail = self.client.get(reverse('catalogo:detalle', args=[self.fumo.slug]))
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.context['fumo'], self.fumo)

        cart = self.client.get(reverse('pedidos:ver'))
        self.assertEqual(cart.status_code, 200)

    def test_admin_catalog_pages_render(self):
        self.client.force_login(self.admin)

        inventory = self.client.get(reverse('catalogo:gestion'))
        self.assertEqual(inventory.status_code, 200)
        self.assertContains(inventory, self.fumo.nombre)

        create = self.client.get(reverse('catalogo:crear'))
        self.assertEqual(create.status_code, 200)

        edit = self.client.get(reverse('catalogo:editar', args=[self.fumo.pk]))
        self.assertEqual(edit.status_code, 200)

        delete = self.client.get(reverse('catalogo:eliminar', args=[self.fumo.pk]))
        self.assertEqual(delete.status_code, 200)
        self.assertContains(delete, self.fumo.nombre)
