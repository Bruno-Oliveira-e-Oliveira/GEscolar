# Generated by Django 2.2.2 on 2019-08-10 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0040_aula'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='turma',
            name='unique_Sala_Turma_Periodo',
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.UniqueConstraint(fields=('Sala', 'Periodo', 'AnoLetivo', 'Escola'), name='unique_Sala_Turma_Periodo'),
        ),
    ]
