# Generated by Django 2.2.2 on 2019-10-06 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0059_auto_20190831_2140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matriz_item',
            options={'verbose_name': 'Item da matriz'},
        ),
        migrations.AlterField(
            model_name='matriz_item',
            name='Serie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Serie', verbose_name='Série'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='Numero',
            field=models.DecimalField(decimal_places=0, max_digits=1, verbose_name='Número'),
        ),
    ]