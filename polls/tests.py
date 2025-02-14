"""from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Producto

constant_cliente_prueba = "Cliente de prueba"
constant_producto_prueba = "Producto de prueba"


# Create your tests here.
class ClienteModelTest(TestCase):

    def test_string_representation(self):
        cliente = Cliente(razon_social=constant_cliente_prueba)
        self.assertEqual(str(cliente), cliente.razon_social)

    def test_to_json(self):
        cliente = Cliente(telefono=123456789, razon_social=constant_cliente_prueba)
        cliente.save()
        expected_json = {
            'id': cliente.id,
            'telefono': cliente.telefono,
            'razon_social': cliente.razon_social
        }
        self.assertEqual(cliente.toJson(), expected_json)

    def test_to_json_bad(self):
        cliente = Cliente(telefono=123456789, razon_social=constant_cliente_prueba)
        cliente.save()
        expected_json = {
            'id': cliente.id,
            'telefono': cliente.telefono,
            'razon': cliente.razon_social
        }
        self.assertNotEqual(cliente.toJson(), expected_json)


class ProductoModelTest(TestCase):
    def test_defaults(self):
        cliente = Cliente.objects.create(razon_social=constant_cliente_prueba)
        producto = Producto.objects.create(descripcion=constant_producto_prueba, precio=100.0, cliente=cliente)
        self.assertEqual(producto.codigo, 0)

    def test_string_representation(self):
        cliente = Cliente.objects.create(razon_social=constant_cliente_prueba)
        producto = Producto.objects.create(codigo=123, descripcion=constant_producto_prueba, precio=100.0,
                                           cliente=cliente)
        self.assertEqual(str(producto), producto.descripcion)


class ProductosListaViewTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(telefono=123456789, razon_social=constant_cliente_prueba)
        self.producto = Producto.objects.create(codigo=123, descripcion=constant_producto_prueba, precio=100.0,
                                                cliente=self.cliente)
        self.client = Client()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('polls_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_post_creates_new_producto(self):
        productos_before = Producto.objects.count()
        response = self.client.post('/', {'codigo': '123', 'descripcion': 'Nuevo Producto', 'precio': '150.00',
                                          'cliente': self.cliente.id})
        productos_after = Producto.objects.count()
        self.assertEqual(productos_after, productos_before + 1)
        self.assertEqual(response.status_code, 302)  # Redirect después del POST

    def test_post_redirects_to_index(self):
        response = self.client.post('/', {'codigo': '123', 'descripcion': 'Nuevo Producto', 'precio': '150.00',
                                          'cliente': self.cliente.id})
        self.assertRedirects(response, '/')
"""