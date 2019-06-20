# Generated by Django 2.2.2 on 2019-06-20 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=20, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rua', models.CharField(max_length=40, verbose_name='Rua')),
                ('Numero', models.PositiveSmallIntegerField(verbose_name='Número')),
                ('Bairro', models.CharField(max_length=40, verbose_name='Bairro')),
                ('Cidade', models.CharField(max_length=40, verbose_name='Cidade')),
                ('Estado', models.CharField(max_length=2, verbose_name='Estado')),
                ('Complemento', models.CharField(max_length=100, verbose_name='Complemento')),
                ('Zona', models.CharField(choices=[('URB', 'Urbana'), ('RUR', 'Rural')], default='URB', max_length=15, verbose_name='Zona')),
            ],
        ),
        migrations.CreateModel(
            name='Escola',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('Email', models.EmailField(max_length=254, verbose_name='Email')),
                ('Nivel_Escolaridade', models.CharField(choices=[('F', 'Ensino Fundamental'), ('M', 'Ensino Médio'), ('FM', 'Ensino Fundamental e Médio')], default='F', max_length=20, verbose_name='Nível Escolaridade')),
                ('Tipo_Escola', models.CharField(choices=[('Pub', 'Pública'), ('Pri', 'Privada')], default='Pub', max_length=20, verbose_name='Tipo da Escola')),
                ('Endereco', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Endereco', verbose_name='Endereço')),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('Sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], default='M', max_length=1, verbose_name='Sexo')),
                ('Data_Nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('Cpf', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='CPF')),
                ('Rg', models.CharField(blank=True, max_length=9, null=True, unique=True, verbose_name='RG')),
                ('Escola', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestaoEscolar.Pessoa')),
                ('Ra', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='RA')),
                ('Cidade_Nascimento', models.CharField(max_length=40, verbose_name='Cidade de Nascimento')),
                ('Estado_Nascimento', models.CharField(max_length=40, verbose_name='Estado de Nascimento')),
                ('Nacionalidade', models.CharField(max_length=20, verbose_name='Nacionalidade')),
                ('Irmao_Gemeo', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='S', max_length=10, verbose_name='Irmão Gêmeo')),
                ('Nome_Pai', models.CharField(max_length=40, verbose_name='Nome do Pai')),
                ('Nome_Mae', models.CharField(max_length=40, verbose_name='Nome da Mãe')),
                ('Necessidade_Educacional_Especial', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='S', max_length=10, verbose_name='Necessidade Educacional Especial')),
                ('Superdotacao', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='S', max_length=10, verbose_name='Superdotação/Altas Habilidades')),
                ('Deficiencia', models.CharField(choices=[('nao_possui', 'Não Possui'), ('multipla', 'Múltipla'), ('cegueira', 'Cegueira'), ('baixa_visao', 'Baixa Visão'), ('surdez_severa_ou_profunda', 'Surdez Severa ou Profunda'), ('surdez_severa_ou_moderada', 'Surdez Leve ou Moderada'), ('surdocegueira', 'Surdocegueira'), ('fisica_paralisia_cerebral', 'Física – Paralisia Cerebral'), ('fisica_cadeirante', 'Física – Cadeirante'), ('fisica_outros', 'Física – Outros'), ('sindrome_de_down', 'Síndrome de Down'), ('intelectual', 'Intelectual')], default='nao_possui', max_length=40, verbose_name='Deficiência')),
                ('Transtorno_Global_do_Desenvolvimento', models.CharField(choices=[('nao_possui', 'Não Possui'), ('autista_infantil', 'Autista Infantil'), ('sindrome_de_asperger', 'Síndrome de Asperger'), ('sindrome_de_rett', 'Síndrome de Rett'), ('transtorno_desintegrativo_de_infancia', 'Transtorno Desintegrativo de Infância')], default='nao_possui', max_length=40, verbose_name='Transtorno Global do Desenvolvimento')),
                ('Bolsa_Familia', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='S', max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('gestaoEscolar.pessoa',),
        ),
        migrations.CreateModel(
            name='Gestor',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestaoEscolar.Pessoa')),
            ],
            options={
                'abstract': False,
            },
            bases=('gestaoEscolar.pessoa',),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestaoEscolar.Pessoa')),
                ('Titulo', models.CharField(choices=[('E', 'Especialista'), ('M', 'Mestre'), ('D', 'Doutor')], default='E', max_length=20, verbose_name='Título')),
            ],
            options={
                'abstract': False,
            },
            bases=('gestaoEscolar.pessoa',),
        ),
        migrations.CreateModel(
            name='Secretaria',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestaoEscolar.Pessoa')),
            ],
            options={
                'abstract': False,
            },
            bases=('gestaoEscolar.pessoa',),
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=20, verbose_name='Nome')),
                ('Periodo', models.CharField(choices=[('M', 'Manhã'), ('T', 'Tarde')], default='M', max_length=20, verbose_name='Período')),
                ('Nivel_Escolaridade', models.CharField(max_length=20, verbose_name='Nível Escolaridade')),
                ('Sala', models.PositiveSmallIntegerField(verbose_name='Sala')),
                ('Max_Alunos', models.PositiveSmallIntegerField(verbose_name='Máximo de Alunos')),
                ('Escola', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
            ],
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero', models.CharField(max_length=20, verbose_name='Número')),
                ('Escola', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
                ('Pessoa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Pessoa', verbose_name='Pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Leciona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Aulas_Previstas', models.PositiveSmallIntegerField(verbose_name='Aulas Previstas')),
                ('Disciplina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Disciplina', verbose_name='Disciplina')),
                ('Escola', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola')),
                ('Turma', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Turma', verbose_name='Turma')),
            ],
        ),
        migrations.AddField(
            model_name='endereco',
            name='Pessoa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Pessoa', verbose_name='Pessoa'),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='Escola',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Escola', verbose_name='Escola'),
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.UniqueConstraint(fields=('Nome', 'Escola'), name='unique_Turma'),
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.UniqueConstraint(fields=('Nome', 'Sala', 'Periodo', 'Escola'), name='unique_Sala_Turma_Periodo'),
        ),
        migrations.AddField(
            model_name='leciona',
            name='Professor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Professor', verbose_name='Professor'),
        ),
        migrations.AddField(
            model_name='escola',
            name='Diretor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Gestor', verbose_name='Diretor'),
        ),
        migrations.AddConstraint(
            model_name='disciplina',
            constraint=models.UniqueConstraint(fields=('Nome', 'Escola'), name='unique_Disciplina'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='Turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestaoEscolar.Turma', verbose_name='Turma'),
        ),
        migrations.AddConstraint(
            model_name='leciona',
            constraint=models.UniqueConstraint(fields=('Disciplina', 'Turma', 'Escola'), name='unique_Leciona'),
        ),
        migrations.AddConstraint(
            model_name='escola',
            constraint=models.UniqueConstraint(fields=('Email',), name='unique_email_escola'),
        ),
        migrations.AddConstraint(
            model_name='escola',
            constraint=models.UniqueConstraint(fields=('Nome', 'Endereco'), name='unique_endereco_escola'),
        ),
    ]
