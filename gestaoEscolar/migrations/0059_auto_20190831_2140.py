# Generated by Django 2.2.2 on 2019-09-01 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0058_aula_bimestre'),
    ]

    operations = [
        migrations.AddField(
            model_name='escola',
            name='Situacao',
            field=models.CharField(choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A', max_length=10, verbose_name='Situação'),
        ),
        migrations.AlterField(
            model_name='frequencia',
            name='Presenca',
            field=models.CharField(choices=[('Presente', 'Presente'), ('Ausente', 'Ausente')], default='Presente', max_length=10, verbose_name='Presenca'),
        ),
    ]
