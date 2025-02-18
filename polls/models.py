from django.db import models
from django.contrib.auth.models import User  # Usar el modelo de usuario predeterminado
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)  # Cambiado para más flexibilidad
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usar User en vez de settings.AUTH_USER_MODEL
    titulo = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField(default="Descripción no disponible")
    imagen = models.ImageField(upload_to='recetas/', null=True, blank=True)
    pasos_de_preparacion = models.TextField()
    categoria = models.CharField(max_length=50)
    dificultad = models.CharField(max_length=50)
    tiempo_de_coccion = models.IntegerField(null=False, blank=False)
    ingredientes = models.ManyToManyField(Ingrediente, through='RecetaIngrediente')
    favoritos = models.ManyToManyField('Perfil', related_name='recetas_favoritas', blank=True)

    def __str__(self):
        return self.titulo

class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.ingrediente.nombre} para {self.receta.titulo}"


class UsuarioReceta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'receta')

    def __str__(self):
        return f"Usuario: {self.usuario} - Receta: {self.receta}"


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario} para {self.receta}"


class ListaDeCompras(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usar User en vez de settings.AUTH_USER_MODEL
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return f"Lista de compras para {self.receta.titulo} - {self.ingrediente.nombre}"


class HistorialCocinado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usar User en vez de settings.AUTH_USER_MODEL
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    fecha_cocinado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} cocinó {self.receta.titulo} el {self.fecha_cocinado}"


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favoritos = models.ManyToManyField('Receta', related_name='favoritos_de_usuario', blank=True)
