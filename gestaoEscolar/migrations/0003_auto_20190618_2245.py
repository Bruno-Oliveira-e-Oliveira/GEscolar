# Generated by Django 2.2.2 on 2019-06-18 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0002_auto_20190618_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='Escola',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola'),
        ),
    ]
