# Generated by Django 2.2.2 on 2019-06-29 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0003_auto_20190629_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endereco',
            name='Pessoa',
        ),
    ]
