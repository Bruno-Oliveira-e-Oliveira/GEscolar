# Generated by Django 2.2.2 on 2019-07-28 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0033_auto_20190728_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='Nome',
            field=models.CharField(max_length=1, verbose_name='Nome'),
        ),
    ]