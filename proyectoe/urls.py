from django.contrib import admin
from django.urls import path
from Modulos.Academico.views import agregar_curso, agregar_docente, agregar_pregunta, calificaciones, index, index_two, juegosplan, login_view, login_viewEstudiante
from Modulos.Academico.views import Listaestudiante, buscarestudiante, agregar_estudiantes, modificar_estudiante, eliminar_estudiante, juegoU, juegoD, juegoAdivinanza, procesar_respuestas
from Modulos.Academico.views import modificar_curso, eliminar_curso, Listacurso
from Modulos.Academico.views import modificar_docente, eliminar_docente, Listadocente, logout_view
from Modulos.Academico.views import modificar_calificaciones, eliminar_calificaciones, Listacalificaciones
from Modulos.Academico.views import Listapreguntas, logout, juegoPregunta, procesar_respuestas_preguntas, agregar_adivinanza


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_two, name='index_two'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('login_viewEstudiante/', login_viewEstudiante, name='login_viewEstudiante'),
    path('juego_adivinanza/', juegoAdivinanza, name='juego_adivinanza'),
    path('procesar_respuestas/', procesar_respuestas, name='procesar_respuestas'),
    path('agregar_estudiantes/', agregar_estudiantes, name='agregar_estudiantes'),   
    path('agregar_curso/', agregar_curso, name='agregar_curso'), 
    path('agregar_docente/', agregar_docente, name='agregar_docente'), 
    path('agregar_pregunta/', agregar_pregunta, name='agregar_pregunta'), 
    path('calificaciones/', calificaciones, name='calificaciones'),
    path('lestudiantes/', Listaestudiante, name='Listaestudiante'),
    path('buscarestudiante/', buscarestudiante),
    path('modificar_estudiante/<int:documento>', modificar_estudiante, name="modificar_estudiante"),
    path('eliminar_estudiante/<int:documento>', eliminar_estudiante, name="eliminar_estudiante"),
    path('lcurso/', Listacurso, name='Listacurso'),
    path('modificar_curso/<int:codCurso>', modificar_curso, name="modificar_curso"),
    path('eliminar_curso/<int:codCurso>', eliminar_curso, name="eliminar_curso"),
    path('ldocente/', Listadocente, name='Listadocente'),
    path('modificar_docente/<int:documento>', modificar_docente, name="modificar_docente"),
    path('eliminar_docente/<int:documento>', eliminar_docente, name="eliminar_docente"),
    path('lcalificaciones/', Listacalificaciones, name='Listacalificaciones'),
    path('modificar_calificaciones/<int:codCalificacion>', modificar_calificaciones, name="modificar_calificaciones"),
    path('eliminar_calificaciones/<int:codCalificacion>', eliminar_calificaciones, name="eliminar_calificaciones"),
    path('lpreguntas/', Listapreguntas, name='Listapreguntas'),
    path("juegoU", juegoU, name='juegoU'),
    path('juegosplan/', juegosplan, name='juegosplan' ),
    path('juego_pregunta/', juegoPregunta, name='juego_pregunta'),
    path('procesar_respuestas_preguntas/', procesar_respuestas_preguntas, name='procesar_respuestas_preguntas'),
    path("agregar_adivinanza/", agregar_adivinanza, name='agregar_adivinanza'),
    path("logout/", logout_view, name='logout_view'),
]
