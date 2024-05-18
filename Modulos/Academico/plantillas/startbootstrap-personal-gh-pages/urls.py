"""proyectoe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Modulos.Academico.views import agregar_curso, agregar_docente, calificaciones, index, index_two, login_view
from Modulos.Academico.views import Listaestudiante, buscarestudiante, agregar_estudiantes, modificar_estudiante, eliminar_estudiante
from Modulos.Academico.views import modificar_curso, eliminar_curso, Listacurso
from Modulos.Academico.views import modificar_docente, eliminar_docente, Listadocente
from Modulos.Academico.views import modificar_calificaciones, eliminar_calificaciones, Listacalificaciones



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('agregar_estudiantes/', agregar_estudiantes, name='agregar_estudiantes'),   
    path('agregar_curso/', agregar_curso, name='agregar_curso'), 
    path('agregar_docente/', agregar_docente, name='agregar_docente'), 
    path('calificaciones/', calificaciones, name='calificaciones'),
    path('index/', index, name='index'),
    path('index_two/', index_two, name='index_two'),
    path('lestudiantes/', Listaestudiante, name='Listaestudiante'),
    path('buscarestudiante/', buscarestudiante),
    path('modificar_estudiante/<int:codEstudiante>', modificar_estudiante, name="modificar_estudiante"),
    path('eliminar_estudiante/<int:codEstudiante>', eliminar_estudiante, name="eliminar_estudiante"),
    path('lcurso/', Listacurso, name='Listacurso'),
    path('modificar_curso/<int:codCurso>', modificar_curso, name="modificar_curso"),
    path('eliminar_curso/<int:codCurso>', eliminar_curso, name="eliminar_curso"),
    path('ldocente/', Listadocente, name='Listadocente'),
    path('modificar_docente/<int:codDocente>', modificar_docente, name="modificar_docente"),
    path('eliminar_docente/<int:codDocente>', eliminar_docente, name="eliminar_docente"),
    path('lcalificaciones/', Listacalificaciones, name='Listacalificaciones'),
    path('modificar_calificaciones/<int:codCalificacion>', modificar_calificaciones, name="modificar_calificaciones"),
    path('eliminar_calificaciones/<int:codCalificacion>', eliminar_calificaciones, name="eliminar_calificaciones"),
]
