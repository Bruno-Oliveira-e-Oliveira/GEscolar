# Generated by Django 2.2.2 on 2019-08-05 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0039_auto_20190801_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Data', models.DateField(verbose_name='Data')),
                ('Escola', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
                ('Leciona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Leciona', verbose_name='Leciona')),
                ('Turma', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Turma', verbose_name='Turma')),
            ],
        ),
    ]
