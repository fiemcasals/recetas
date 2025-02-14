from .models import Usuario
from django import forms
from .models import Receta, Ingrediente
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Receta, RecetaIngrediente, Ingrediente


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


class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username','email', 'fecha_nacimiento', 'password1', 'password2']


    # Validación personalizada para la contraseña, si deseas más seguridad
    def clean_password(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Agregar reglas adicionales para la contraseña aquí
        return cleaned_data

    # Validación personalizada para el campo 'email', si es necesario
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Aquí puedes agregar validación para evitar duplicados u otros requisitos
        return email

class LoginForm(forms.Form):
        username = forms.CharField(max_length=100, label="Nombre de usuario")
        password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")



from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }


#lista de compras

class SeleccionarRecetasForm(forms.Form):
    recetas = forms.ModelMultipleChoiceField(
        queryset=Receta.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecciona las recetas"
    )
