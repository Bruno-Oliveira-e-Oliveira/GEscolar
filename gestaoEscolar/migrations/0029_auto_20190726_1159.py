# Generated by Django 2.2.2 on 2019-07-26 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0028_auto_20190721_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula_turma',
            name='Situacao',
            field=models.CharField(choices=[('matriculado', 'Matriculado'), ('concluido', 'Concluído'), ('transferido', 'Transferido'), ('trancado', 'Trancado')], default='matriculado', max_length=20, verbose_name='Situação'),
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero', models.DecimalField(decimal_places=0, max_digits=1, verbose_name='Numero')),
                ('Nivel_Escolaridade', models.CharField(choices=[('F', 'Ensino Fundamental'), ('M', 'Ensino Médio')], default='F', max_length=20, verbose_name='Nível Escolaridade')),
                ('Escola', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
            ],
        ),
        migrations.CreateModel(
            name='Matriz_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Carga', models.DecimalField(decimal_places=0, max_digits=2, verbose_name='Carga')),
                ('Disciplina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Disciplina', verbose_name='Disciplina')),
                ('Escola', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
                ('Serie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Serie', verbose_name='Serie')),
            ],
        ),
        migrations.AddConstraint(
            model_name='serie',
            constraint=models.UniqueConstraint(fields=('Numero', 'Nivel_Escolaridade', 'Escola'), name='unique_Serie_NVE_Escola'),
        ),
        migrations.AddConstraint(
            model_name='matriz_item',
            constraint=models.UniqueConstraint(fields=('Serie', 'Disciplina', 'Escola'), name='unique_Serie_Disciplina_Escola'),
        ),
    ]
