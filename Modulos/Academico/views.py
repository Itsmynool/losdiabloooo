import random
import os
import json
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.conf import settings
from .models import Estudiante
from .models import Docente
from .models import Curso
from .models import Calificacion
from .models import Preguntas
from .models import Adivinanzas, Puntuacion
from .forms import EstudiantesForm
from .forms import CursoForm
from .forms import DocenteForm
from .forms import CalificacionesForm, AdivinanzasForm
from .forms import LoginForm
from .forms import PreguntasForm
from .forms import LoginFormEstudiante
from django.contrib import messages
from random import choice
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404


#Nuevo para PDF
from io import BytesIO
from django.template import context
from django.template.loader import get_template
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesize import A4, cm
#from __future__ import unicode_literals

#Para Busqueda
from django.db.models import Q


#abrir
from io import open


def index(request):
    return render(request, '')


def login_estudiante(request):
    if request.method == 'POST':
        form = LoginFormEstudiante(request.POST)
        if form.is_valid():
            codigo_estudiante = form.cleaned_data['codigo_estudiante']
            documento = form.cleaned_data['documento']

            estudiante = authenticate(codigo_estudiante=codigo_estudiante, documento=documento)
            if estudiante is not None:
                login(request, estudiante)
                return redirect('index')
            else:
                messages.error(request, 'Credenciales inválidas.')
    else:
        form = LoginFormEstudiante()

    return render(request, 'loginEstudiante.html', {'form': form})

def agregar_estudiantes(request):
	data={
		'form': EstudiantesForm()
	}

	if request.method =='POST':
		formulario = EstudiantesForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="guardado correctamente"
		else:
			data["form"]=formulario
			data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarestudiante.html', data)

import logging
from django.contrib.auth.hashers import check_password
logger = logging.getLogger(__name__)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            user = authenticate(request, username=correo, password=password)  # Cambiado de 'correo' a 'username'
            if user is not None:
                login(request, user)
                return redirect('index')  # Cambia 'index' por la URL a la que deseas redirigir después del inicio de sesión
            else:
                print("Credenciales incorrectas")
        else:
            print("Formulario no válido")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Cambiar 'nombre_de_la_vista_de_inicio_de_sesion' por el nombre de la vista de inicio de sesión

def login_viewEstudiante(request):
    print("Método de solicitud:", request.method)  # Agrega este print para mostrar el método de la solicitud
    if request.method == 'POST':
        form = LoginFormEstudiante(request.POST)
        print("FORM IS VALID: ", form.is_valid())
        if form.is_valid():
            documento = form.cleaned_data['documento']
            password = form.cleaned_data['password']
            # Autenticar al estudiante utilizando el número de documento y la contraseña
            user = authenticate(request, documento=documento, password=password)
            if user is not None:
                login(request, user)
                # Redirigir a la página después de iniciar sesión
                return redirect('index')  # Cambia 'index' por la URL a la que deseas redirigir después del inicio de sesión
            else:
                # Maneja el caso en que la autenticación falle
                print("Credenciales incorrectas.")
                messages.error(request, 'Credenciales incorrectas.')
                # Aquí puedes agregar más lógica o redirigir a una página de error, según sea necesario
    else:
        form = LoginFormEstudiante()
    return render(request, 'loginEstudiante.html', {'form': form})

def juegoAdivinanza(request):
    puntuacionObj = ''
    print(request.user)
    if request.method == 'POST':
        total_adivinanzas = Adivinanzas.objects.count()
        return render(request, 'juegoAdivinanza.html', {'adivinanzas': None, 'total_adivinanzas': total_adivinanzas})

    if 'reiniciar' in request.GET:
        puntuacionObj = Puntuacion(estudiante=request.user, puntuacion=request.session.get('puntaje', 0), tipo_de_juego='Adivinanza' )
        puntuacionObj.save()
        request.session.pop('adivinanzas_mostradas', None)
        request.session.pop('puntaje', None)
        return redirect('juego_adivinanza')

    adivinanzas_mostradas = request.session.get('adivinanzas_mostradas', [])
    todas_las_adivinanzas = list(Adivinanzas.objects.all())
    adivinanzas_restantes = [adivinanza for adivinanza in todas_las_adivinanzas if adivinanza.id not in adivinanzas_mostradas]

    print("TODAS: ", len(todas_las_adivinanzas))
    print("RESTANTES: ", len(adivinanzas_mostradas))

    if adivinanzas_restantes:
        adivinanza = choice(adivinanzas_restantes)
        adivinanza.opciones = adivinanza.opciones.split(',')
        adivinanzas_mostradas.append(adivinanza.id)
        request.session['adivinanzas_mostradas'] = adivinanzas_mostradas
        puntaje = request.session.get('puntaje', 0)
        return render(request, 'juegoAdivinanza.html', {'adivinanzas': adivinanza, 'puntaje': puntaje})

    total_adivinanzas = Adivinanzas.objects.count()
    puntaje = request.session.get('puntaje', 0)
    #puntuacionObj = Puntuacion(estudiante=request.user, puntuacion=puntaje, tipo_de_juego='Adivinanza' )
    #puntuacionObj.save()
    return render(request, 'juegoAdivinanza.html', {'adivinanzas': None, 'puntaje': puntaje, 'total_adivinanzas': total_adivinanzas})

def procesar_respuestas(request):
    if request.method == 'POST':
        adivinanzas_mostradas = request.session.get('adivinanzas_mostradas', [])
        puntaje = request.session.get('puntaje', 0)
        for adivinanza_id in adivinanzas_mostradas:
            respuesta_seleccionada = request.POST.get(f'respuesta{adivinanza_id}', '').strip()
            try:
                adivinanza = Adivinanzas.objects.get(pk=adivinanza_id)
            except Adivinanzas.DoesNotExist:
                raise Http404("La adivinanza solicitada no existe")
            if respuesta_seleccionada.lower() == adivinanza.respuesta_correcta.strip().lower():
                puntaje += 1
        request.session['puntaje'] = puntaje
        return redirect('juego_adivinanza')

    return redirect('juego_adivinanza')


def juegoPregunta(request):
    puntuacionObj=''
    if request.method == 'POST':
        total_preguntas = Preguntas.objects.count()
        return render(request, 'juegoPregunta.html', {'preguntas': None, 'total_preguntas': total_preguntas})

    if 'reiniciar' in request.GET:
        puntuacionObj = Puntuacion(estudiante=request.user, puntuacion=request.session.get('puntaje', 0), tipo_de_juego='Preguntas' )
        puntuacionObj.save()
        request.session.pop('preguntas_mostradas', None)
        request.session.pop('puntaje', None)
        return redirect('juego_pregunta')

    preguntas_mostradas = request.session.get('preguntas_mostradas', [])
    todas_las_preguntas = list(Preguntas.objects.all())
    preguntas_restantes = [pregunta for pregunta in todas_las_preguntas if pregunta.id not in preguntas_mostradas]

    if preguntas_restantes:
        pregunta = choice(preguntas_restantes)
        pregunta.opciones = pregunta.opciones.split(',')
        preguntas_mostradas.append(pregunta.id)
        request.session['preguntas_mostradas'] = preguntas_mostradas
        puntaje = request.session.get('puntaje', 0)
        return render(request, 'juegoPregunta.html', {'preguntas': pregunta, 'puntaje': puntaje})

    total_preguntas = Preguntas.objects.count()
    puntaje = request.session.get('puntaje', 0)
    return render(request, 'juegoPregunta.html', {'preguntas': None, 'puntaje': puntaje, 'total_preguntas': total_preguntas})

def procesar_respuestas_preguntas(request):
    if request.method == 'POST':
        preguntas_mostradas = request.session.get('preguntas_mostradas', [])
        puntaje = request.session.get('puntaje', 0)
        for pregunta_id in preguntas_mostradas:
            respuesta_seleccionada = request.POST.get(f'respuesta{pregunta_id}', '').strip()
            pregunta = Preguntas.objects.get(pk=pregunta_id)
            if respuesta_seleccionada.lower() == pregunta.respuesta_correcta.strip().lower():
                puntaje += 1
        request.session['puntaje'] = puntaje
        return redirect('juego_pregunta')

    return redirect('juego_pregunta')


def agregar_curso(request):
	data={
		'form': CursoForm()
	}

	if request.method =='POST':
		formulario = CursoForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="guardado correctamente"
		else:
			data["form"]=formulario
			data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarcurso.html', data)

def agregar_docente(request):
	data={
		'form': DocenteForm()
	}

	if request.method =='POST':
		formulario = DocenteForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="guardado correctamente"
		else:
			data["form"]=formulario
			data["mensaje"]="el archivo ya existe"
	return render(request, 'agregardocente.html', data)

def agregar_pregunta(request):
	data={
		'form': PreguntasForm()
	}

	if request.method =='POST':
		formulario = PreguntasForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="guardado correctamente"
		else:
			data["form"]=formulario
			data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarpregunta.html', data)

def agregar_adivinanza(request):
	data={
		'form': AdivinanzasForm()
	}

	if request.method =='POST':
		formulario = AdivinanzasForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="guardado correctamente"
		else:
			data["form"]=formulario
			data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarpregunta.html', data)

def Listaadivinanzas(request):
	Listaadivinanzas=Adivinanzas.objects.all()
	return render(request, "listaadivinanzas.html",{"Adivinanzas":Listaadivinanzas})

def eliminar_adivinanzas(request, adivinanza_id):
    adivinanza = get_object_or_404(Adivinanzas, id=adivinanza_id)
    adivinanza.delete()
    messages.success(request, "Adivinanza eliminada correctamente")
    return redirect(to='Listaadivinanzas')

def modificar_adivinanzas(request, adivinanza_id):
	adivinanza=get_object_or_404(Adivinanzas, id=adivinanza_id)#busca un elemento
	data={
		'form':AdivinanzasForm(instance=adivinanza)
	}

	if request.method=='POST':
		formulario=AdivinanzasForm(data=request.POST, instance=adivinanza, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado Correctamente")
			data["mensaje"]="Archivo Modificado"
			return redirect(to='../ladivinanzas')
		else:
			data["form"]=formulario
			data["mensaje"]="El archivo no existe"
			return redirect(to='Listaadivinanzas')
	return render(request, 'modificarAdivinanza.html', data)

def calificaciones(request):
	data={
		'form': CalificacionesForm()
	}

	if request.method =='POST':
		formulario = CalificacionesForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="guardado correctamente"
		else:
			data["form"]=formulario
			data["mensaje"]="el archivo ya existe"
	return render(request, 'calificaciones.html', data)

@login_required(login_url='/login/')  
def index(request):
    return render(request, "index.html",{})     

def Listaestudiante(request):
    Listaestudiante=Estudiante.objects.all()
    return render(request, "listaestudiante.html",{"Estudiantes":Listaestudiante})

def Listacurso(request):
	Listacurso=Curso.objects.all()
	print("HOOLAAAAAAAAAAAAAAAAAAAAAAAAA: ", Listacurso)
	return render(request, "listacurso.html",{"Curso":Listacurso})

def Listadocente(request):
    print("HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    Listadocente=Docente.objects.all()
    print("HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", Listadocente)
    return render(request, "listadocentes.html",{"Docente":Listadocente})

def Listacalificaciones(request):
	Listacalificaciones=Calificacion.objects.all()
	return render(request, "listacalificaciones.html",{"Calificaciones":Listacalificaciones})

def Listapreguntas(request):
	Listapreguntas=Preguntas.objects.all()
	return render(request, "listapreguntas.html",{"Preguntas":Listapreguntas})

def buscarestudiante(request):
	busqueda=request.GET.get("buscar")
	estudiante=Estudiante.objects.all()
	if busqueda:
		estudiante = Estudiante.objects.filter(
			Q(codEstudiante__icontains = busqueda) | #or (o)
			Q(nombres__icontains = busqueda) |
			Q(primerApellido__icontains = busqueda) | #__icontains para que no sea exacto
			Q(segundoApellido__icontains = busqueda) |#__icontains para que no sea exacto
			Q(documento__icontains = busqueda) |#__icontains para que no sea exacto
			Q(fechaNacimiento__icontains = busqueda) |#__icontains para que no sea exacto
			Q(genero__icontains = busqueda) #__icontains para que no sea exacto
			).distinct()

	return render(request, "listaestudiante.html", {"estudiante":estudiante})

def modificar_estudiante(request, documento):
	estudiantes=get_object_or_404(Estudiante, documento=documento)#busca un elemento

	data={
		'form':EstudiantesForm(instance=estudiantes)
	}

	if request.method=='POST':
		formulario=EstudiantesForm(data=request.POST, instance=estudiantes, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado Correctamente")
			data["mensaje"]="Archivo Modificado"
			return redirect(to='../lestudiantes')
		else:
			data["form"]=formulario
			data["mensaje"]="El archivo no existe"
			return redirect(to='Listaestudiante')
	return render(request, 'modificar.html', data)

def eliminar_estudiante(request, documento):
	estudiantes = get_object_or_404(Estudiante, documento=documento)
	estudiantes.delete()
	messages.success(request, "Eliminado Correctamente")
	
	return render(request, 'listaestudiante.html', {'eliminar': True})
	


def buscarCurso(request):
	busqueda=request.GET.get("buscar")
	Curso=Curso.objects.all()
	if busqueda:
		Curso = Curso.objects.filter(
			Q(curso__icontains = busqueda) | #or (o)
			Q(codCurso__icontains = busqueda) #__icontains para que no sea exacto
			).distinct()

	return render(request, "listacurso.html", {"Curso":Curso})

def modificar_curso(request, codCurso):
	curso=get_object_or_404(Curso, codCurso=codCurso)#busca un elemento

	data={
		'form':CursoForm(instance=curso)
	}

	if request.method=='POST':
		formulario=CursoForm(data=request.POST, instance=curso, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado Correctamente")
			data["mensaje"]="Archivo Modificado"
		else:
			data["form"]=formulario
			data["mensaje"]="El archivo no existe"
			return redirect(to='Listacurso')
		data["form"]=formulario
	return render(request, 'modificarcurso.html', data)

def eliminar_curso(request, codCurso):
	curso = get_object_or_404(Curso, codCurso=codCurso)
	curso.delete()
	messages.success(request, "Eliminado Correctamente")
	return redirect(to='Listacurso')



def modificar_docente(request, codDocente):
	docente=get_object_or_404(Docente, codDocente=codDocente)#busca un elemento

	data={
		'form':DocenteForm(instance=docente)
	}

	if request.method=='POST':
		formulario=DocenteForm(data=request.POST, instance=docente, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado Correctamente")
			data["mensaje"]="Archivo Modificado"
		else:
			data["form"]=formulario
			data["mensaje"]="El archivo no existe"
			return redirect(to='Listadocente')
		data["form"]=formulario
	return render(request, 'modificardocente.html', data)

def eliminar_docente(request, documento):
	docente = get_object_or_404(Docente, documento=documento)
	docente.delete()
	messages.success(request, "Eliminado Correctamente")
	return redirect(to='Listadocente')

def buscarCalificacion(request):
	busqueda=request.GET.get("buscar")
	calificaciones=Calificacion.objects.all()
	if busqueda:
		calificaciones = Calificacion.objects.filter(
			Q(codCalificacion__icontains = busqueda) | #or (o)
			Q(actividad__icontains = busqueda) |
			Q(codEstudiante__nombres__icontains = busqueda) |
			Q(calificacion__icontains = busqueda) 
			).distinct()

	return render(request, "listacalificaciones.html", {"Calificaciones":calificaciones})

def modificar_calificaciones(request, codCalificacion):
	calificaciones=get_object_or_404(Calificacion, codCalificacion=codCalificacion)#busca un elemento

	data={
		'form':CalificacionesForm(instance=calificaciones)
	}

	if request.method=='POST':
		formulario=CalificacionesForm(data=request.POST, instance=calificaciones, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado Correctamente")
			data["mensaje"]="Archivo Modificado"
		else:
			data["form"]=formulario
			data["mensaje"]="El archivo no existe"
			return redirect(to='Listacalificaciones')
		data["form"]=formulario
	return render(request, 'modificarcalificaciones.html', data)

def eliminar_calificaciones(request, codCalificacion):
	calificaciones = get_object_or_404(Calificacion, codCalificacion=codCalificacion)
	calificaciones.delete()
	messages.success(request, "Eliminado Correctamente")
	return redirect(to='Listacalificaciones')


def juegoU(request):

	if request.method=='POST':
		point = 0
		if request.POST["flexRadioDefault2"] == "true":
			point += 1
		if request.POST["flexRadioDefault2"] == "true":
			point += 1
		if request.POST["flexRadioDefault3"] == "true":
			point += 1
		if request.POST["flexRadioDefault4"] == "true":
			point += 1
		if request.POST["flexRadioDefault5"] == "true":
			point += 1
		if request.POST["flexRadioDefault6"] == "true":
			point += 1
		if request.POST["flexRadioDefault7"] == "true":
			point += 1
		if request.POST["flexRadioDefault8"] == "true":
			point += 1
		if request.POST["flexRadioDefault9"] == "true":
			point += 1
		if request.POST["flexRadioDefault10"] == "true":
			point += 1
		data={
			"pointt":point
		}
		return render(request, "puntuacion.html", data)

	return render(request, "juegoU.html")

def juegoD(request):

	if request.method=='POST':
		point = 0
		if request.POST["flexRadioDefault2"] == "true":
			point += 1
		if request.POST["flexRadioDefault2"] == "true":
			point += 1
		if request.POST["flexRadioDefault3"] == "true":
			point += 1
		if request.POST["flexRadioDefault4"] == "true":
			point += 1
		if request.POST["flexRadioDefault5"] == "true":
			point += 1
		if request.POST["flexRadioDefault6"] == "true":
			point += 1
		if request.POST["flexRadioDefault7"] == "true":
			point += 1
		if request.POST["flexRadioDefault8"] == "true":
			point += 1
		if request.POST["flexRadioDefault9"] == "true":
			point += 1
		if request.POST["flexRadioDefault10"] == "true":
			point += 1
		data={
			"pointt":point
		}
		return render(request, "puntuacion.html", data)

	return render(request, "juegoD.html")

def index_two(request):
    return render(request, "indextwo.html",{})    

def juegosplan(request):
    return render(request, "startbootstrap-personal-gh-pages/projects.html",{})    

def eliminar_preguntas(request, pregunta_id):
    pregunta = get_object_or_404(Preguntas, id=pregunta_id)
    pregunta.delete()
    messages.success(request, "Pregunta eliminada correctamente")
    return redirect(to='Listapreguntas')

def modificar_preguntas(request, pregunta_id):
	pregunta=get_object_or_404(Preguntas, id=pregunta_id)#busca un elemento
	data={
		'form':PreguntasForm(instance=pregunta)
	}

	if request.method=='POST':
		formulario=PreguntasForm(data=request.POST, instance=pregunta, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado Correctamente")
			data["mensaje"]="Archivo Modificado"
			return redirect(to='../lpreguntas')
		else:
			data["form"]=formulario
			data["mensaje"]="El archivo no existe"
			return redirect(to='Listapreguntas')
	return render(request, 'modificarPregunta.html', data)