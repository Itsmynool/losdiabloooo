# Generated by Django 4.2.7 on 2024-05-18 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0007_remove_calificacion_id_calificacion_codcalificacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField()),
                ('tipo_de_juego', models.CharField(choices=[('M', 'Memoria'), ('P', 'Preguntas'), ('A', 'Adivinanza')], max_length=1)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academico.estudiante')),
            ],
        ),
    ]
