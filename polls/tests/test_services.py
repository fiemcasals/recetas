#las pruebas sirven para probar metodos, por ahora no quiero probar ninguno
# y estas pruebas son pruebas modelos del profe acorde a su trabajo

"""from django.test import TestCase

from polls.models import Cliente, Producto
from polls.services import ProductoService


class ProductoServiceTest(TestCase):

    def setUp(self):
        Cliente.objects.create(telefono=123456789, razon_social="Cliente Test")
        cliente = Cliente.objects.first()
        Producto.objects.create(codigo=1, descripcion="Producto Test", precio=10.0, cliente=cliente)

    def test_obtener_productos_y_calculos(self):
        productos, calculos = ProductoService.obtener_productos_y_calculos()
        self.assertEqual(productos.count(), 1)
        self.assertIsNotNone(calculos['peep'])
        self.assertIsNotNone(calculos['coco'])"""
