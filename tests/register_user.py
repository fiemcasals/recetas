from django.test import TestCase                  
from django.urls import reverse      # Permite obtener URLs a partir de sus nombres.
from django.contrib.auth.models import User       

class RegistroFormTest(TestCase):
    
    def setUp(self):
        # Se ejecuta antes de cada prueba.
        # Se define la URL de la vista de registro usando el nombre asignado en urls.py ('registro').
        self.url = reverse('registro')

    def test_registro_usuario_exitoso(self):
        """Prueba de registro exitoso de un nuevo usuario."""
        
        # Define datos válidos para el registro.
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        print("Enviando datos de registro:", data)  # Imprimir los datos enviados para el registro.

        # Envía una solicitud POST a la URL de registro.
        response = self.client.post(self.url, data)
       
        # Verifica que la respuesta redirige a la URL de lista de recetas.
        self.assertRedirects(response, reverse('lista_recetas'))
        
        # Verifica que se haya creado el usuario en la base de datos.
        user = User.objects.get(username='testuser')
        print("Usuario creado:", user)  # Imprimir el usuario creado.

        # Verifica que el email es correcto.
        self.assertEqual(user.email, 'testuser@example.com')
        print("Email verificado:", user.email)

        # Verifica que la contraseña se haya guardado correctamente (usando check_password).
        if self.assertTrue(user.check_password('TestPassword123')):
            print("Contraseña verificada correctamente.")


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

"""
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
"""