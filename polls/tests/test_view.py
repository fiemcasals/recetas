#las pruebas sirven para probar metodos, por ahora no quiero probar ninguno
# y estas pruebas son pruebas modelos del profe acorde a su trabajo

#Las clases de prueba como ProductosListaViewTest son llamadas por el propio framework de pruebas de Django cuando ejecutas el comando python manage.py test.

#Si alguna prueba falla, Django proporciona información detallada sobre el error.

#falta entender la sintaxis de cada caso

"""from django.test import Client
from django.test import TestCase
from django.urls import reverse

from polls.models import Cliente, Producto


class ProductosListaViewTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(telefono=123456789, razon_social="Cliente Test")
        self.producto = Producto.objects.create(codigo=1, descripcion="Producto Test", precio=10.0,
                                                cliente=self.cliente)
        self.client = Client()

    def test_get_context_data(self):
        response = self.client.get(reverse('polls_index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('resultado', response.context)
        self.assertIn('data', response.context)
        self.assertIn('sumaProducto', response.context)
        self.assertIn('cliente', response.context)

    def test_post(self):
        post_data = {
            'cliente': self.cliente.id,
            'codigo': '2',
            'descripcion': 'Otro Producto',
            'precio': '20'
        }
        response = self.client.post(reverse('polls_index'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirección después de POST
        self.assertEqual(Producto.objects.count(), 2)"""
