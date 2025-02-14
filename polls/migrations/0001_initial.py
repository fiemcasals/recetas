# Generated by Django 5.1.3 on 2025-02-13 01:33

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=5)),
                ('unidad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(default='Descripción no disponible')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='recetas/')),
                ('pasos_de_preparacion', models.TextField()),
                ('categoria', models.CharField(max_length=50)),
                ('dificultad', models.CharField(max_length=50)),
                ('tiempo_de_coccion', models.IntegerField()),
                ('favoritos', models.ManyToManyField(blank=True, related_name='favoritos_recetas', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('calificacion', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario_comentador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_realizados', to=settings.AUTH_USER_MODEL)),
                ('usuario_receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recetas_notificaciones', to=settings.AUTH_USER_MODEL)),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_receta', to='polls.receta')),
            ],
        ),
        migrations.CreateModel(
            name='ListaDeCompras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=5)),
                ('unidad', models.CharField(max_length=50)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.ingrediente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.receta')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialCocinado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cocinado', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.receta')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('calificacion', models.PositiveIntegerField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to=settings.AUTH_USER_MODEL)),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='polls.receta')),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='favoritos',
            field=models.ManyToManyField(blank=True, related_name='usuarios_favoritos', to='polls.receta'),
        ),
        migrations.CreateModel(
            name='RecetaIngrediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=5)),
                ('unidad', models.CharField(max_length=50)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.ingrediente')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.receta')),
            ],
        ),
        migrations.AddField(
            model_name='receta',
            name='ingredientes',
            field=models.ManyToManyField(blank=True, through='polls.RecetaIngrediente', to='polls.ingrediente'),
        ),
        migrations.CreateModel(
            name='UsuarioReceta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receta_usuarios', to='polls.receta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_recetas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'receta')},
            },
        ),
    ]
