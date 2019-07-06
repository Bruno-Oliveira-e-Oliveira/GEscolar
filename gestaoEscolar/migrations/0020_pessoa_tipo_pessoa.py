# Generated by Django 2.2.2 on 2019-07-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaoEscolar', '0019_remove_gestor_tipo_gestor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='Tipo_Pessoa',
            field=models.CharField(choices=[('G', 'Gestor'), ('D', 'Diretor'), ('S', 'Secretário'), ('P', 'Professor'), ('A', 'Aluno')], default='D', max_length=20, verbose_name='Tipo de Pessoa'),
            preserve_default=False,
        ),
    ]