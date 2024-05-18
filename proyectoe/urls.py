from django.contrib import admin
from django.urls import path
from Modulos.Academico.views import agregar_curso, agregar_docente, agregar_pregunta, calificaciones, index, index_two, juegosplan, login_view, login_viewEstudiante
from Modulos.Academico.views import Listaestudiante, buscarestudiante, agregar_estudiantes, modificar_estudiante, eliminar_estudiante, juegoU, juegoD, juegoAdivinanza, procesar_respuestas
from Modulos.Academico.views import modificar_curso, eliminar_curso, Listacurso, eliminar_preguntas, Listaadivinanzas
from Modulos.Academico.views import modificar_docente, eliminar_docente, Listadocente, logout_view, modificar_preguntas, eliminar_adivinanzas
from Modulos.Academico.views import modificar_calificaciones, eliminar_calificaciones, Listacalificaciones, buscarCalificacion
from Modulos.Academico.views import Listapreguntas, puntuaciones, juegoPregunta, procesar_respuestas_preguntas, agregar_adivinanza, modificar_adivinanzas


urlpatterns = [
    # Estudiante
    path('agregar_estudiantes/', agregar_estudiantes, name='agregar_estudiantes'),
    path('lestudiantes/', Listaestudiante, name='Listaestudiante'),
    path('buscarestudiante/', buscarestudiante),
    path('modificar_estudiante/<int:documento>', modificar_estudiante, name="modificar_estudiante"),
    path('eliminar_estudiante/<int:documento>', eliminar_estudiante, name="eliminar_estudiante"),

    # Docente
    path('agregar_docente/', agregar_docente, name='agregar_docente'), 
    path('ldocente/', Listadocente, name='Listadocente'),
    path('modificar_docente/<int:documento>', modificar_docente, name="modificar_docente"),
    path('eliminar_docente/<int:documento>', eliminar_docente, name="eliminar_docente"),

    # Curso
    path('agregar_curso/', agregar_curso, name='agregar_curso'), 
    path('lcurso/', Listacurso, name='Listacurso'),
    path('eliminar_curso/<int:codCurso>', eliminar_curso, name="eliminar_curso"),
    path('modificar_curso/<int:codCurso>', modificar_curso, name="modificar_curso"),

    path('procesar_respuestas/', procesar_respuestas, name='procesar_respuestas'),
    path("juegoU", juegoU, name='juegoU'),
    path('juegosplan/', juegosplan, name='juegosplan' ),

    # Preguntas
    path('juego_pregunta/', juegoPregunta, name='juego_pregunta'),
    path('agregar_pregunta/', agregar_pregunta, name='agregar_pregunta'),
    path('lpreguntas/', Listapreguntas, name='Listapreguntas'),
    path('eliminar_preguntas/<int:pregunta_id>/', eliminar_preguntas, name="eliminar_preguntas"),
    path('procesar_respuestas_preguntas/', procesar_respuestas_preguntas, name='procesar_respuestas_preguntas'),
    path('modificar_preguntas/<int:pregunta_id>', modificar_preguntas, name="modificar_preguntas"),

    # Calificaciones
    path('buscarCalificacion/', buscarCalificacion, name="buscarCalificacion"),
    path('lcalificaciones/', Listacalificaciones, name='Listacalificaciones'),
    path('calificaciones/', calificaciones, name='calificaciones'),
    path('modificar_calificaciones/<int:codCalificacion>', modificar_calificaciones, name="modificar_calificaciones"),
    path('eliminar_calificaciones/<int:codCalificacion>', eliminar_calificaciones, name="eliminar_calificaciones"),

    # Adivinanza
    path('juego_adivinanza/', juegoAdivinanza, name='juego_adivinanza'),
    path('agregar_adivinanza/', agregar_adivinanza, name='agregar_adivinanza'),
    path('procesar_respuestas/', procesar_respuestas, name='procesar_respuestas'),
    path('ladivinanza/', Listaadivinanzas, name='Listaadivinanzas'),
    path('eliminar_adivinanzas/<int:adivinanza_id>/', eliminar_adivinanzas, name="eliminar_adivinanzas"),
    path('modificar_adivinanzas/<int:adivinanza_id>', modificar_adivinanzas, name="modificar_adivinanzas"),

    # Index
    path('index/', index, name='index'),
    path('', index_two, name='index_two'),

    # Otros
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('login_viewEstudiante/', login_viewEstudiante, name='login_viewEstudiante'),

    # Puntuaciones
    path('puntuaciones/', puntuaciones, name='puntuaciones'),
]
