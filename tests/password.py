from django.test import TestCase                  
from django.urls import reverse      # Permite obtener URLs a partir de sus nombres.
from django.contrib.auth.models import User       

class RegistroFormTest(TestCase):
    
    def setUp(self):
        # Se ejecuta antes de cada prueba.
        # Se define la URL de la vista de registro usando el nombre asignado en urls.py ('registro').
        self.url = reverse('registro')

    def test_contraseñas_no_coinciden(self):
        """Prueba que falla el registro cuando las contraseñas no coinciden."""
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'WrongPassword123'
        }
        print("Datos enviados para prueba de contraseñas no coinciden:", data)  # Imprimir los datos enviados.

        response = self.client.post(self.url, data)
        response.render()  # Fuerza el renderizado para que se genere el contexto.
        
        # Extrae el formulario del contexto de la respuesta.
        form = response.context.get('form')
                
        self.assertIsNotNone(form, "No se encontró el formulario en el contexto.")
        self.assertTrue(form.is_bound)
        print("Formulario está vinculado:", form.is_bound)

        # Verifica que en el campo 'password2' aparezca el error esperado.
        print("Errores en 'password1':", form.errors.get('password1', []))
        print("Errores en 'password2':", form.errors.get('password2', []))
