#las pruebas sirven para probar metodos, por ahora no quiero probar ninguno
# y estas pruebas son pruebas modelos del profe acorde a su trabajo

"""#TestCase permite hacer afirmaciones y configurar el entorno de pruebas, entre otras funcionalidades.
from django.test import TestCase
#Importa los modelos Cliente y Producto desde el archivo models.py de la aplicación polls. Estos modelos representan las tablas en la base de datos.
from polls.models import Cliente, Producto
#Esta clase parece ser responsable de la lógica relacionada con los productos, como obtener y agregar productos.
from polls.repository import ProductoRepository


class ProductoRepositoryTest(TestCase):

    def setUp(self):
        Cliente.objects.create(telefono=123456789, razon_social="Cliente Test")
        cliente = Cliente.objects.first()
        Producto.objects.create(codigo=1, descripcion="Producto Test", precio=10.0, cliente=cliente)

    def test_obtener_todos(self):
        productos = ProductoRepository.obtener_todos()
        self.assertEqual(productos.count(), 1)
        self.assertEqual(productos.first().descripcion, "Producto Test")

    def test_agregar_producto(self):
        cliente = Cliente.objects.first()
        ProductoRepository.agregar_producto(2, "Nuevo Producto", 20.0, cliente.id)
        self.assertEqual(Producto.objects.count(), 2)"""
