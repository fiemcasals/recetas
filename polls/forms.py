from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import modelformset_factory
from .models import Receta, Ingrediente, Comentario
from django.contrib.auth.models import User 

# Formularios para las recetas e ingredientes
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'descripcion', 'imagen', 'pasos_de_preparacion', 'categoria', 'dificultad', 'tiempo_de_coccion']


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'cantidad', 'unidad']
     
# Crear un formset para los ingredientes
IngredienteFormSet = modelformset_factory(Ingrediente, form=IngredienteForm, extra=1)



from django.core.exceptions import ValidationError

# Formulario de registro que usa el modelo User de Django
class RegistroForm(UserCreationForm):
    class Meta:
        model = User  # Usamos el modelo User de Django
        fields = ['username', 'email', 'password1', 'password2']

    # Validación personalizada para las contraseñas
    def clean_password(self):
        # Se obtiene la data limpia usando el método 'clean' del formulario
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        # Aquí se pueden agregar reglas adicionales para la contraseña si se desea
        return cleaned_data

    # Validación personalizada para el campo 'email'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica que el email no se encuentre ya registrado
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email


# Formulario de inicio de sesión
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,  # Cambiado a True para que sea obligatorio
        initial="Usuario"  # Equivalente a default="Usuario"
    )
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")


# Formulario para comentarios
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }


# Formulario para seleccionar recetas
class SeleccionarRecetasForm(forms.Form):
    recetas = forms.ModelMultipleChoiceField(
        queryset=Receta.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecciona las recetas"
    )
