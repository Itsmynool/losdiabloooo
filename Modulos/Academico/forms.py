from django import forms
from .models import Curso, Docente, Estudiante, Calificacion, Preguntas, Adivinanzas, Memoria

class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo electrónico', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class LoginFormEstudiante(forms.Form):
    documento = forms.CharField(label='Código de estudiante', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class CursoForm(forms.ModelForm):

	class Meta:
		model = Curso
		fields = '__all__'

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['nombre_completo', 'correo', 'documento']

class EstudiantesForm(forms.ModelForm):

	class Meta:
		model = Estudiante
		fields = ['first_name', 'last_name', 'username', 'email', 'fecha_nacimiento', 'genero', 'curso']

class CalificacionesForm(forms.ModelForm):

	class Meta:
		model = Calificacion
		fields = '__all__'

class PreguntasForm(forms.ModelForm):

	class Meta:
		model = Preguntas
		fields = '__all__'

class AdivinanzasForm(forms.ModelForm):

	class Meta:
		model = Adivinanzas
		fields = '__all__'

class MemoriaForm(forms.ModelForm):

	class Meta:
		model = Memoria
		fields = '__all__'