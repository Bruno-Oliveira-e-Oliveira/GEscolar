from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from gestaoEscolar.forms import *
from gestaoEscolar.models import *
from .permissoes import checarPermEscola, checarPermObj, limpar_grupos, configurar_grupos
from .login import salvar_escola_pessoa_sessao

@login_required
def aluno_listagem(request):
    request = salvar_escola_pessoa_sessao(request)
    checarPermObj('gestaoEscolar.view_aluno', request.user)
    try:
        status = request.GET['ativo']
        matricula = request.GET['matricula']
    except Exception as erro:
        status = 'Todos'
        matricula = 'Todos'

    STATUS = (
        ('Todos', 'Todos'),
        ('True', 'Ativo'),
        ('False', 'Inativo')
    )
    TIPOS_SITUACAO = (
        ('Todos', 'Todos'),
        ('matriculado', 'Matriculado'),
        ('concluido', 'Concluído'),
        ('transferido', 'Transferido'),
        ('trancado', 'Trancado')
    )
    escola = Escola.objects.get(id=request.session['Escola'])
    alunos = Pessoa.obter_pessoa_por_status('Aluno',status,escola)
    alunos = Aluno.filtrar_matriculas(alunos, matricula)
    matriculas = Matricula.objects.filter(Escola=escola.id)

    context = {
        'alunos': alunos, 
        'matriculas': matriculas,
        'Filtro_Status': STATUS, 
        'status': status,
        'Filtro_Matricula': TIPOS_SITUACAO,
        'matricula': matricula
    }
    return render(request, 'gestaoEscolar/aluno/aluno_listagem.html', context)



@login_required
def aluno_novo(request):
    checarPermObj('gestaoEscolar.add_aluno', request.user)
    TIPO_SEXO = Aluno.TIPO_SEXO
    STATUS = Aluno.STATUS
    SIM_NAO = Aluno.SIM_NAO
    TIPOS_DEFICIENCIA = Aluno.TIPOS_DEFICIENCIA
    TIPOS_TRANSTORNO = Aluno.TIPOS_TRANSTORNO
    TIPOS_SITUACAO = Matricula.TIPOS_SITUACAO
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO, 
            'Tipo_Status': STATUS,
            'Sim_Nao':  SIM_NAO,
            'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
            'Tipos_Transtorno': TIPOS_TRANSTORNO,
            'Tipos_Situacao': TIPOS_SITUACAO,
            'zonas': ZONAS, 
            'Tipo_Transacao': 'INS'
        }
        return render(request,'gestaoEscolar/aluno/aluno_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'],
            'is_active': dados['is_active']
        }
        aluno_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'],
            'Ra': dados['Ra'],
            'Cidade_Nascimento': dados['Cidade_Nascimento'],
            'Estado_Nascimento': dados['Estado_Nascimento'],
            'Nacionalidade': dados['Nacionalidade'],
            'Irmao_Gemeo': dados['Irmao_Gemeo'],
            'Nome_Pai': dados['Nome_Pai'],
            'Nome_Mae': dados['Nome_Mae'],
            'Necessidade_Educacional_Especial': dados['Necessidade_Educacional_Especial'],
            'Superdotacao': dados['Superdotacao'],
            'Deficiencia': dados['Deficiencia'],
            'Transtorno_Global_do_Desenvolvimento': dados['Transtorno_Global_do_Desenvolvimento'],
            'Bolsa_Familia': dados['Bolsa_Familia'],
            'Turma': '',
            'Usuario': '',
            'Endereco': '',
            'Tipo_Pessoa': 'A',
            'Telefone': '',
            'Escola': ''
        }
        endereco_dados = {
            'Rua': dados['Rua'], 
            'Numero': dados['Numero'], 
            'Bairro': dados['Bairro'], 
            'Cidade': dados['Cidade'], 
            'Estado': dados['Estado'], 
            'Complemento': dados['Complemento'],
            'Zona': dados['Zona']
        }
        telefone_dados = {
            'Numero1': dados['Numero1'], 
            'Numero2': dados['Numero2']
        }

        aluno_form = AlunoForm(aluno_dados)
        usuario_form = UsuarioEmailForm(usuario_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone_form = TelefoneForm(telefone_dados)
        erros_aluno = {}
        erros_usuario = {}
        erros_matricula = {}
        erros_endereco = {}
        erros_telefone = {}

        if not aluno_form.is_valid():
            erros_aluno = aluno_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone1_form.errors

        if erros_aluno or erros_endereco or erros_telefone or erros_usuario:
            erros = []
            for erro in erros_aluno.values():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)                
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            context = {
                'Tipo_Sexo': TIPO_SEXO, 
                'Tipo_Status': STATUS,
                'Sim_Nao':  SIM_NAO,
                'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
                'Tipos_Transtorno': TIPOS_TRANSTORNO,
                'Tipos_Situacao': TIPOS_SITUACAO,
                'zonas': ZONAS, 
                'erros':erros, 
                'aluno_dados':aluno_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'INS'
            }
            return render(request,'gestaoEscolar/aluno/aluno_form.html', context)
        else:
            try:
                with transaction.atomic():
                    #Criar o nome de usuario a partir do RG e CPF 
                    # (fazê-los obrigatórios nos cadastros exceto Diretores)
                    nome_usuario = dados['Ra'] + dados['Estado']
                    senha = dados['Cpf']
                    usuario = User.objects.create_user(
                        nome_usuario, 
                        dados['email'], 
                        senha
                    )
                    usuario.is_active = dados['is_active']                
                    usuario.save()
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    aluno_dados['Usuario'] = usuario.id
                    aluno_dados['Telefone'] = telefone.id
                    aluno_dados['Endereco'] = endereco.id
                    escola = Escola.objects.get(id=request.session['Escola'])
                    aluno_dados['Escola'] = escola.id
                    aluno_form = AlunoForm(aluno_dados)
                    aluno = aluno_form.save()
                    matricula = Matricula(
                        Data=timezone.now(),
                        Aluno=aluno,
                        Escola=escola
                    )
                    matricula.save()
                    #Configurando o grupo
                    configurar_grupos('A',usuario)
                    return redirect('aluno_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipo_Sexo': TIPO_SEXO, 
                    'Tipo_Status': STATUS,
                    'Sim_Nao':  SIM_NAO,
                    'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
                    'Tipos_Transtorno': TIPOS_TRANSTORNO,
                    'Tipos_Situacao': TIPOS_SITUACAO,
                    'zonas': ZONAS, 
                    'erros':erros, 
                    'aluno_dados':aluno_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/aluno/aluno_form.html', context)


@login_required
def aluno_alterar(request,id):
    checarPermObj('gestaoEscolar.change_aluno', request.user)
    aluno_obj = get_object_or_404(Aluno, id=id)
    checarPermEscola(aluno_obj, Escola.objects.get(id=request.session['Escola']))
    endereco_obj = Endereco.objects.get(id=aluno_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=aluno_obj.Telefone.id)
    matricula_obj = Matricula.objects.get(Aluno=aluno_obj.id)
    usuario_obj = User.objects.get(id=aluno_obj.Usuario.id)
    TIPO_SEXO = Aluno.TIPO_SEXO
    STATUS = Aluno.STATUS
    SIM_NAO = Aluno.SIM_NAO
    TIPOS_DEFICIENCIA = Aluno.TIPOS_DEFICIENCIA
    TIPOS_TRANSTORNO = Aluno.TIPOS_TRANSTORNO
    TIPOS_SITUACAO = Matricula.TIPOS_SITUACAO
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO, 
            'Tipo_Status': STATUS,
            'Sim_Nao':  SIM_NAO,
            'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
            'Tipos_Transtorno': TIPOS_TRANSTORNO,
            'Tipos_Situacao': TIPOS_SITUACAO,
            'zonas': ZONAS, 
            'aluno_dados': aluno_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'usuario_dados': usuario_obj,
            'matricula_dados': matricula_obj,
            'Tipo_Transacao': 'UPD',
            'idAluno': id
        }
        return render(request,'gestaoEscolar/aluno/aluno_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'],
            'is_active': dados['is_active']
        }
        aluno_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'],
            'Ra': dados['Ra'],
            'Cidade_Nascimento': dados['Cidade_Nascimento'],
            'Estado_Nascimento': dados['Estado_Nascimento'],
            'Nacionalidade': dados['Nacionalidade'],
            'Irmao_Gemeo': dados['Irmao_Gemeo'],
            'Nome_Pai': dados['Nome_Pai'],
            'Nome_Mae': dados['Nome_Mae'],
            'Necessidade_Educacional_Especial': dados['Necessidade_Educacional_Especial'],
            'Superdotacao': dados['Superdotacao'],
            'Deficiencia': dados['Deficiencia'],
            'Transtorno_Global_do_Desenvolvimento': dados['Transtorno_Global_do_Desenvolvimento'],
            'Bolsa_Familia': dados['Bolsa_Familia'],
            'Usuario': aluno_obj.Usuario.id,
            'Endereco': aluno_obj.Endereco.id,
            'Tipo_Pessoa': aluno_obj.Tipo_Pessoa,
            'Telefone': aluno_obj.Telefone.id,
            'Escola': aluno_obj.Escola.id
        }
        matricula_dados = {
            'Situacao': dados['Situacao']
        }
        endereco_dados = {
            'Rua': dados['Rua'], 
            'Numero': dados['Numero'], 
            'Bairro': dados['Bairro'], 
            'Cidade': dados['Cidade'], 
            'Estado': dados['Estado'], 
            'Complemento': dados['Complemento'],
            'Zona': dados['Zona']
        }
        telefone_dados = {
            'Numero1': dados['Numero1'], 
            'Numero2': dados['Numero2']
        }
        aluno_form = AlunoForm(aluno_dados , instance=aluno_obj)
        matricula_form = MatriculaForm(matricula_dados , instance=matricula_obj)
        usuario_form = UsuarioEmailForm(usuario_dados, instance=usuario_obj)
        endereco_form = EnderecoForm(endereco_dados, instance=endereco_obj)
        telefone_form = TelefoneForm(telefone_dados, instance=telefone_obj)
        erros_aluno = {}
        erros_matricula = {}
        erros_usuario = {}
        erros_endereco = {}
        erros_telefone = {}

        if not aluno_form.is_valid():
            erros_aluno = aluno_form.errors

        if not matricula_form.is_valid():
            erros_matricula = matricula_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_aluno or erros_endereco or erros_telefone or erros_usuario or erros_matricula:
            erros = []
            for erro in erros_aluno.values():
                erros.append(erro)
            for erro in erros_matricula.values():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)               
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            matricula_dados['Rm'] = matricula_obj.Rm
            matricula_dados['Data'] = matricula_obj.Data
            context = {
                'Tipo_Sexo': TIPO_SEXO, 
                'Tipo_Status': STATUS,
                'Sim_Nao':  SIM_NAO,
                'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
                'Tipos_Transtorno': TIPOS_TRANSTORNO,
                'Tipos_Situacao': TIPOS_SITUACAO,
                'zonas': ZONAS, 
                'erros':erros, 
                'aluno_dados':aluno_dados, 
                'matricula_dados': matricula_dados,
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'UPD',
                'idAluno': id
            }
            return render(request,'gestaoEscolar/aluno/aluno_form.html', context)
        else:
            try:
                with transaction.atomic():
                    usuario = usuario_form.save()
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    aluno = aluno_form.save()
                    matricula = matricula_form.save()
                    return redirect('aluno_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                matricula_dados['Rm'] = matricula_obj.Rm
                matricula_dados['Data'] = matricula_obj.Data
                context = {
                    'Tipo_Sexo': TIPO_SEXO, 
                    'Tipo_Status': STATUS,
                    'Sim_Nao':  SIM_NAO,
                    'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
                    'Tipos_Transtorno': TIPOS_TRANSTORNO,
                    'Tipos_Situacao': TIPOS_SITUACAO,
                    'zonas': ZONAS, 
                    'erros':erros, 
                    'aluno_dados':aluno_dados, 
                    'matricula_dados': matricula_dados,
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'UPD',
                    'idAluno': id
                }
                return render(request,'gestaoEscolar/aluno/aluno_form.html', context)


@login_required
def aluno_consultar(request,id):
    checarPermObj('gestaoEscolar.view_aluno', request.user)
    aluno_obj = get_object_or_404(Aluno, id=id)
    checarPermEscola(aluno_obj, Escola.objects.get(id=request.session['Escola']))
    matricula_obj = Matricula.objects.get(Aluno=aluno_obj.id)
    endereco_obj = Endereco.objects.get(id=aluno_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=aluno_obj.Telefone.id)
    usuario_obj = User.objects.get(id=aluno_obj.Usuario.id)
    TIPO_SEXO = Aluno.TIPO_SEXO
    STATUS = Aluno.STATUS
    SIM_NAO = Aluno.SIM_NAO
    TIPOS_DEFICIENCIA = Aluno.TIPOS_DEFICIENCIA
    TIPOS_TRANSTORNO = Aluno.TIPOS_TRANSTORNO
    TIPOS_SITUACAO = Matricula.TIPOS_SITUACAO
    ZONAS = Endereco.TIPOS_ZONAS
    context = {
        'Tipo_Sexo': TIPO_SEXO, 
        'Tipo_Status': STATUS,
        'Sim_Nao':  SIM_NAO,
        'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
        'Tipos_Transtorno': TIPOS_TRANSTORNO,
        'Tipos_Situacao': TIPOS_SITUACAO,
        'zonas': ZONAS, 
        'aluno_dados': aluno_obj,
        'matricula_dados': matricula_obj,
        'endereco_dados': endereco_obj,       
        'telefone_dados': telefone_obj,
        'usuario_dados': usuario_obj,
        'Tipo_Transacao': 'CON',
        'idAluno': id
    }
    return render(request,'gestaoEscolar/aluno/aluno_form.html', context)


@login_required
def aluno_deletar(request,id):
    checarPermObj('gestaoEscolar.delete_aluno', request.user)
    aluno_obj = get_object_or_404(Aluno, id=id)
    checarPermEscola(aluno_obj, Escola.objects.get(id=request.session['Escola']))
    endereco_obj = Endereco.objects.get(id=aluno_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=aluno_obj.Telefone.id)
    matricula_obj = Matricula.objects.get(Aluno=aluno_obj.id)
    usuario_obj = User.objects.get(id=aluno_obj.Usuario.id)
    TIPO_SEXO = Aluno.TIPO_SEXO
    STATUS = Aluno.STATUS
    SIM_NAO = Aluno.SIM_NAO
    TIPOS_DEFICIENCIA = Aluno.TIPOS_DEFICIENCIA
    TIPOS_TRANSTORNO = Aluno.TIPOS_TRANSTORNO
    TIPOS_SITUACAO = Matricula.TIPOS_SITUACAO
    ZONAS = Endereco.TIPOS_ZONAS
    escola = Escola.objects.get(id=request.session['Escola'])
    erros = []
    bloqueio = False
    matriculas_turma = Matricula_Turma.objects.filter(Aluno=aluno_obj.id, Escola=escola.id)

    if len(matriculas_turma) > 0:
        erros.append(
            'Não foi possível apagar o aluno pois ele tem referência com matrículas em turmas.'
        )
        bloqueio = True       

    if request.method == 'GET':
        context = {
            'erros': erros,
            'bloqueio': bloqueio,
            'Tipo_Sexo': TIPO_SEXO, 
            'Tipo_Status': STATUS,
            'Sim_Nao':  SIM_NAO,
            'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
            'Tipos_Transtorno': TIPOS_TRANSTORNO,
            'Tipos_Situacao': TIPOS_SITUACAO,
            'zonas': ZONAS, 
            'aluno_dados': aluno_obj,
            'matricula_dados': matricula_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'usuario_dados': usuario_obj,
            'Tipo_Transacao': 'DEL',
            'idAluno': id
        }
        return render(request,'gestaoEscolar/aluno/aluno_form.html', context)
    else:
        try:
            with transaction.atomic():
                limpar_grupos(usuario_obj)
                matricula_obj.delete()
                aluno_obj.delete()
                endereco_obj.delete()
                telefone_obj.delete()
                usuario_obj.delete()
                return redirect('aluno_listagem')
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'Tipo_Sexo': TIPO_SEXO, 
                'Tipo_Status': STATUS,
                'Sim_Nao':  SIM_NAO,
                'Tipos_Deficiencia': TIPOS_DEFICIENCIA,
                'Tipos_Transtorno': TIPOS_TRANSTORNO,
                'Tipos_Situacao': TIPOS_SITUACAO,
                'zonas': ZONAS, 
                'bloqueio': bloqueio,
                'erros':erros, 
                'aluno_dados': aluno_obj,
                'matricula_dados': matricula_obj,
                'endereco_dados': endereco_obj,       
                'telefone_dados': telefone_obj,
                'usuario_dados': usuario_obj,
                'Tipo_Transacao': 'DEL',
                'idAluno': id
            }
            return render(request,'gestaoEscolar/aluno/aluno_form.html', context)


@login_required
def historico(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    idEscola = request.session['Escola']
    matriculas = Matricula_Turma.objects.filter(Aluno=aluno.id, Escola=idEscola)
    context = {'aluno':aluno, 'matriculas':matriculas}
    return render(request,'gestaoEscolar/aluno/historico.html', context)
