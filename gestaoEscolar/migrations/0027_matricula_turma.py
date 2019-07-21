# Generated by Django 2.2.2 on 2019-07-21 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0026_auto_20190721_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matricula_Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Aluno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Aluno', verbose_name='Aluno')),
                ('Escola', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
                ('Turma', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Turma', verbose_name='Turma')),
            ],
        ),
    ]
