from django.db import models
from django.utils import timezone
import random

# Create your models here.
class Curso(models.Model):
    curso=models.CharField(max_length=6, primary_key=True)
    codCurso=models.CharField(max_length=25)

    def __str__(self):
        txt="{0}, Cod:{1}"
        return txt.format(self.curso, self.codCurso)


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.db import models

class DocenteManager(BaseUserManager):
    def create_user(self, correo, contraseña=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio para crear un usuario.')
        user = self.model(correo=self.normalize_email(correo), **extra_fields)
        user.set_password(contraseña)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, contraseña=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        return self.create_user(correo, contraseña, **extra_fields)

class Docente(AbstractBaseUser, PermissionsMixin):
    nombre_completo = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    documento = models.CharField(max_length=12, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='docente_groups', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField(Permission, related_name='docente_permissions', blank=True, verbose_name='user permissions')

    objects = DocenteManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre_completo']

    def __str__(self):
        return self.nombre_completo

from django.contrib.auth.models import AbstractUser

class Estudiante(AbstractUser):
    documento = models.CharField(max_length=12, unique=True)
    fecha_nacimiento = models.CharField(max_length=20)
    generos = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ]
    curso = models.ForeignKey(Curso, null=False, blank=False, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1, choices=generos)
    groups = models.ManyToManyField(Group, related_name='estudiante_groups', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField(Permission, related_name='estudiante_permissions', blank=True, verbose_name='user permissions')

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['username', 'email', 'fecha_nacimiento', 'genero', 'curso']

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.username}"


class Calificacion(models.Model):
    codCalificacion=models.CharField(max_length=1, primary_key=True)
    nombre_actividad = [
        ('M', 'Memoria'),
        ('P', 'Preguntas'),
        ('A', 'Adivinanza'),
    ]
    actividad = models.CharField(max_length=1, choices=nombre_actividad)
    estudiante = models.ForeignKey(Estudiante, null=False, blank=False, on_delete=models.CASCADE)
    calificacion = models.CharField(max_length=5)

    def __str__(self):
        return f"Actividad: {self.actividad} / Nombre estudiante: {self.estudiante} / Calificacion: {self.calificacion}"


class Preguntas(models.Model):
    enunciado = models.CharField(max_length=200)
    respuesta_correcta = models.CharField(max_length=100)
    opciones = models.CharField(max_length=500)

    def __str__(self):
        return f"Pregunta: {self.enunciado}"

    @classmethod
    def obtener_preguntas_aleatorias(cls, cantidad=10):
        todas_preguntas = cls.objects.all()
        preguntas_seleccionadas = random.sample(list(todas_preguntas), min(cantidad, todas_preguntas.count()))
        return preguntas_seleccionadas
    
class Adivinanzas(models.Model):
    enunciado = models.CharField(max_length=200)
    respuesta_correcta = models.CharField(max_length=100)
    opciones = models.CharField(max_length=500)

    def __str__(self):
        return f"Adivinanza {self.id}: {self.enunciado}"

    @classmethod
    def obtener_adivinanzas_aleatorias(cls, cantidad=10):
        todas_adivinanzas = cls.objects.all()
        adivinanzas_seleccionadas = random.sample(list(todas_adivinanzas), min(cantidad, todas_adivinanzas.count()))
        return adivinanzas_seleccionadas
    
class Puntuacion(models.Model):
    TIPOS_DE_JUEGO = [
        ('M', 'Memoria'),
        ('P', 'Preguntas'),
        ('A', 'Adivinanza'),
    ]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    tipo_de_juego = models.CharField(max_length=1, choices=TIPOS_DE_JUEGO)

    def __str__(self):
        return f"Puntuación de {self.estudiante}: {self.puntuacion} ({self.get_tipo_de_juego_display()})"



class Card(models.Model):
    word = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)
