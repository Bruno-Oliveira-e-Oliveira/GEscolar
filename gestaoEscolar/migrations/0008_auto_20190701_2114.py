# Generated by Django 2.2.2 on 2019-07-01 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0007_auto_20190701_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='Numero',
            field=models.IntegerField(error_messages={'max_value': 'Certifique-se que o valor do campo "Número" seja menor ou igual a 4294967295.'}, verbose_name='Número'),
        ),
    ]
