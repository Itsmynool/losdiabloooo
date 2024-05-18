from django.contrib.auth.backends import BaseBackend
from .models import Docente, Estudiante

class DocenteBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            docente = Docente.objects.get(correo=username)
            if docente.password == password:
                return docente
        except Docente.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Docente.objects.get(pk=user_id)
        except Docente.DoesNotExist:
            return None

class EstudianteBackend(BaseBackend):
    def authenticate(self, request, documento=None, password=None):
        try:
            estudiante = Estudiante.objects.get(documento=documento)
            if estudiante.password == password:
                return estudiante
        except Estudiante.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Estudiante.objects.get(pk=user_id)
        except Estudiante.DoesNotExist:
            return None