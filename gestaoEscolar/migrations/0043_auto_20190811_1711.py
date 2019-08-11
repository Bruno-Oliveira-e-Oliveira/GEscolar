# Generated by Django 2.2.2 on 2019-08-11 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0042_aula_tema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Presenca', models.BooleanField(default=True, verbose_name='Presença')),
                ('Aluno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Aluno', verbose_name='Aluno')),
                ('Aula', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Aula', verbose_name='Aula')),
                ('Escola', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
            ],
        ),
        migrations.AddConstraint(
            model_name='frequencia',
            constraint=models.UniqueConstraint(fields=('Aula', 'Aluno'), name='unique_Aula_Aluno'),
        ),
    ]
