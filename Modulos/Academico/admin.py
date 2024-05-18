from django.contrib import admin
from .models import Docente, Estudiante, Curso, Calificacion, Preguntas, Card, Adivinanzas, Puntuacion

# Register your models here.

admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Curso)
admin.site.register(Calificacion)
admin.site.register(Preguntas)
admin.site.register(Card)
admin.site.register(Adivinanzas)
admin.site.register(Puntuacion)
