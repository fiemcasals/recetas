from django.test import TestCase                  
from django.urls import reverse      # Permite obtener URLs a partir de sus nombres.
from django.contrib.auth.models import User       

class RegistroFormTest(TestCase):
    
    def setUp(self):
        # Se ejecuta antes de cada prueba.
        # Se define la URL de la vista de registro usando el nombre asignado en urls.py ('registro').
        self.url = reverse('registro')

    
    def test_formulario_invalido(self):
        #Prueba que el formulario falla cuando se envían datos incompletos o incorrectos.
        data = {
            'username': '',            # Campo de nombre de usuario vacío.
            'email': 'invalidemail',   # Email con formato incorrecto.
            'password1': 'short',      # Contraseña demasiado corta.
            'password2': 'short'       # Contraseña demasiado corta.
        }
        print("Datos enviados para prueba de formulario inválido:", data)  # Imprimir los datos enviados.

        response = self.client.post(self.url, data)
        response.render()  # Fuerza el renderizado para que se genere el contexto.
        
        form = response.context.get('form')
        print("Formulario en contexto:", form)  # Imprimir el formulario obtenido del contexto.

        self.assertIsNotNone(form, "No se encontró el formulario en el contexto.")
        self.assertTrue(form.is_bound)
        print("Formulario está vinculado:", form.is_bound)

        # Verifica que en el campo 'username' se muestre el error de campo obligatorio.
        self.assertIn("Este campo es obligatorio.", form.errors.get('username', []))
        print("Errores en 'username':", form.errors.get('username', []))  # Imprimir los errores de 'username'

        # Verifica que en el campo 'email' se muestre el error de formato.
        self.assertTrue(
            any("introduzca una dirección de correo electrónico válida" in msg.lower() for msg in form.errors.get('email', [])),
            "El error esperado para el email no se encontró."
        )
        print("Errores en 'email':", form.errors.get('email', []))  # Imprimir los errores de 'email'

        # Combina los errores de 'password1' y los errores no asociados (non_field_errors)
        errors_password = form.errors.get('password1', []) + list(form.non_field_errors())
        print("Errores en 'password1' y non_field_errors:", errors_password)  # Imprimir los errores combinados.

        # Verifica que alguno de esos mensajes contenga "demasiado corta".
        self.assertTrue(
            any("demasiado corta" in msg.lower() for msg in errors_password),
            "El error esperado para password1 no se encontró."
        )
