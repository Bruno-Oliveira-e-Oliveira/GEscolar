# Generated by Django 2.2.2 on 2019-07-05 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0018_auto_20190702_2234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gestor',
            name='Tipo_Gestor',
        ),
    ]