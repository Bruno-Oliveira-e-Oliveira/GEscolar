# Generated by Django 2.2.2 on 2019-07-01 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0006_auto_20190701_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escola',
            name='Endereco',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Endereco', verbose_name='Endereço'),
            preserve_default=False,
        ),
    ]
