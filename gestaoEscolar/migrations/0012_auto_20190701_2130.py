# Generated by Django 2.2.2 on 2019-07-01 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0011_auto_20190701_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escola',
            name='Nota_de_Corte',
            field=models.DecimalField(decimal_places=0, error_messages={'max_whole_digits': 'Valor inválido para o campo Nota.'}, max_digits=1, verbose_name='Nota de corte de aprovação'),
        ),
    ]
