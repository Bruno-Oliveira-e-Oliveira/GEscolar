# Generated by Django 2.2.2 on 2019-07-21 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0023_bimestre_situacao'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='turma',
            name='unique_Turma',
        ),
        migrations.AddField(
            model_name='turma',
            name='AnoLetivo',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.AnoLetivo', verbose_name='Ano'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.UniqueConstraint(fields=('Nome', 'AnoLetivo', 'Escola'), name='unique_Turma_Ano'),
        ),
    ]
