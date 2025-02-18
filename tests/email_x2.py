from django.test import TestCase                  
from django.urls import reverse      # Permite obtener URLs a partir de sus nombres.
from django.contrib.auth.models import User       

class RegistroFormTest(TestCase):
    
    def setUp(self):
        # Se ejecuta antes de cada prueba.
        # Se define la URL de la vista de registro usando el nombre asignado en urls.py ('registro').
        self.url = reverse('registro')

    
    def test_email_duplicado(self):
        #Prueba que falla el registro si el email ya está registrado.
        # Crea un usuario con el email a utilizar en la prueba.
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='TestPassword123')
        print("Usuario 'existinguser' creado con el email 'testuser@example.com'")  # Confirmar creación del usuario.

        data = {
            'username': 'newuser',
            'email': 'testuser@example.com',
            'password1': 'NewPassword123',
            'password2': 'NewPassword123'
        }
        print("Datos enviados para prueba de email duplicado:", data)  # Imprimir los datos enviados.

        response = self.client.post(self.url, data)
        response.render()  # Fuerza el renderizado para que se genere el contexto.
        
        # Extrae el formulario del contexto de la respuesta.
        form = response.context.get('form')
              
        self.assertIsNotNone(form, "No se encontró el formulario en el contexto.")
        self.assertTrue(form.is_bound)
        print("Formulario está vinculado:", form.is_bound)

        # Verifica que en el campo 'email' aparezca el error esperado de email duplicado.
        self.assertIn("Este email ya está registrado.", form.errors.get('email', []))
        print("Errores en 'email':", form.errors.get('email', []))  # Imprimir los errores de 'email'
