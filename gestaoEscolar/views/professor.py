from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from gestaoEscolar.forms import *
from gestaoEscolar.models import *
from .permissoes import checarPermEscola
       
@login_required
def professor_listagem(request):
    pessoa = Pessoa.obter_pessoa(request.user.username,'Pessoa')
    if (pessoa is not None) and (pessoa.Escola is not None):
        professores = Professor.objects.filter(Escola=pessoa.Escola).order_by('Nome')
        context = {'professores': professores}
        return render(request, 'gestaoEscolar/professor/professor_listagem.html', context)
    else:
        #Pessoa sem escola ou nome de usuario vazio 
        #Tratar depois
        return HttpResponse('Não foi encontrada nenhuma associação com uma escola')


@login_required
def professor_novo(request):
    TIPO_SEXO = Professor.TIPO_SEXO
    STATUS = Professor.STATUS
    TIPOS_TITULOS = Professor.TIPOS_TITULOS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO, 
            'Tipo_Titulos': TIPOS_TITULOS, 
            'Tipo_Status': STATUS, 
            'zonas': ZONAS, 
            'Tipo_Transacao': 'INS'
        }
        return render(request,'gestaoEscolar/professor/professor_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'],
            'is_active': dados['is_active']
        }
        professor_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'],
            'Titulo': dados['Titulo'],
            'Usuario': '',
            'Endereco': '',
            'Tipo_Pessoa': 'P',
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
        professor_form = ProfessorForm(professor_dados)
        usuario_form = UsuarioEmailForm(usuario_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone_form = TelefoneForm(telefone_dados)
        erros_professor = {}
        erros_usuario = {}
        erros_endereco = {}
        erros_telefone = {}

        if not professor_form.is_valid():
            erros_professor = professor_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone1_form.errors

        if erros_professor or erros_endereco or erros_telefone or erros_usuario:
            erros = []
            for erro in erros_professor.values():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)               
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            context = {
                'Tipo_Sexo': TIPO_SEXO,
                'Tipo_Titulos': TIPOS_TITULOS, 
                'zonas': ZONAS,
                'Tipo_Status': STATUS,
                'erros':erros, 
                'professor_dados':professor_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'INS'
            }
            return render(request,'gestaoEscolar/professor/professor_form.html', context)
        else:
            try:
                with transaction.atomic():
                    #Criar o nome de usuario a partir do RG e CPF 
                    # (fazê-los obrigatórios nos cadastros exceto Diretores)
                    nome_usuario = dados['Rg'] + dados['Estado']
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
                    professor_dados['Usuario'] = usuario.id
                    professor_dados['Telefone'] = telefone.id
                    professor_dados['Endereco'] = endereco.id
                    escola = Escola.objects.get(id=request.session['Escola'])
                    professor_dados['Escola'] = escola.id
                    professor_form = ProfessorForm(professor_dados)
                    professor = professor_form.save()
                    return redirect('professor_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipo_Sexo': TIPO_SEXO,
                    'Tipo_Titulos': TIPOS_TITULOS, 
                    'Tipo_Status': STATUS,
                    'zonas': ZONAS,
                    'erros':erros, 
                    'professor_dados':professor_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/professor/professor_form.html', context)


@login_required
def professor_alterar(request,id):
    professor_obj = Professor.objects.get(id=id)
    endereco_obj = Endereco.objects.get(id=professor_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=professor_obj.Telefone.id)
    usuario_obj = User.objects.get(id=professor_obj.Usuario.id)
    TIPO_SEXO = Professor.TIPO_SEXO
    TIPOS_TITULOS = Professor.TIPOS_TITULOS
    STATUS = Professor.STATUS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO,
            'Tipo_Titulos': TIPOS_TITULOS,
            'Tipo_Status': STATUS,
            'zonas': ZONAS,
            'professor_dados': professor_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'usuario_dados': usuario_obj,
            'Tipo_Transacao': 'UPD',
            'idProfessor': id
        }
        return render(request,'gestaoEscolar/professor/professor_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'],
            'is_active': dados['is_active']
        }
        professor_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'], 
            'Titulo': dados['Titulo'],
            'Usuario': professor_obj.Usuario.id, 
            'Endereco': professor_obj.Endereco.id,
            'Tipo_Pessoa': professor_obj.Tipo_Pessoa,
            'Telefone': professor_obj.Telefone.id,
            'Escola': professor_obj.Escola.id
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
        professor_form = ProfessorForm(professor_dados , instance=professor_obj)
        usuario_form = UsuarioEmailForm(usuario_dados, instance=usuario_obj)
        endereco_form = EnderecoForm(endereco_dados, instance=endereco_obj)
        telefone_form = TelefoneForm(telefone_dados, instance=telefone_obj)
        erros_professor = {}
        erros_usuario = {}
        erros_endereco = {}
        erros_telefone = {}

        if not professor_form.is_valid():
            erros_professor = professor_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_professor or erros_endereco or erros_telefone or erros_usuario:
            erros = []
            for erro in erros_professor.values():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)               
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            context = {
                'Tipo_Sexo': TIPO_SEXO,
                'Tipo_Titulos': TIPOS_TITULOS,
                'Tipo_Status': STATUS,
                'zonas': ZONAS,
                'erros':erros, 
                'professor_dados':professor_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'UPD',
                'idProfessor': id
            }
            return render(request,'gestaoEscolar/professor/professor_form.html', context)
        else:
            try:
                with transaction.atomic():
                    usuario = usuario_form.save()
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    professor = professor_form.save()
                    return redirect('professor_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipo_Sexo': TIPO_SEXO,
                    'Tipo_Titulos': TIPOS_TITULOS,
                    'Tipo_Status': STATUS,
                    'zonas': ZONAS,
                    'erros':erros, 
                    'professor_dados':professor_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'UPD',
                    'idProfessor': id
                }
                return render(request,'gestaoEscolar/professor/professor_form.html', context)


@login_required
def professor_consultar(request,id):
    professor_obj = Professor.objects.get(id=id)
    endereco_obj = Endereco.objects.get(id=professor_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=professor_obj.Telefone.id)
    usuario_obj = User.objects.get(id=professor_obj.Usuario.id)
    TIPO_SEXO = Professor.TIPO_SEXO
    TIPOS_TITULOS = Professor.TIPOS_TITULOS
    STATUS = Professor.STATUS
    ZONAS = Endereco.TIPOS_ZONAS
    context = {
        'Tipo_Sexo': TIPO_SEXO,
        'Tipo_Titulos': TIPOS_TITULOS,
        'zonas': ZONAS,
        'Tipo_Status': STATUS,
        'professor_dados': professor_obj,
        'endereco_dados': endereco_obj,       
        'telefone_dados': telefone_obj,
        'usuario_dados': usuario_obj,
        'Tipo_Transacao': 'CON',
        'idProfessor': id
    }
    return render(request,'gestaoEscolar/professor/professor_form.html', context)


@login_required
def professor_deletar(request,id):
    professor_obj = Professor.objects.get(id=id)
    endereco_obj = Endereco.objects.get(id=professor_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=professor_obj.Telefone.id)
    usuario_obj = User.objects.get(id=professor_obj.Usuario.id)
    TIPO_SEXO = Professor.TIPO_SEXO
    TIPOS_TITULOS = Professor.TIPOS_TITULOS
    STATUS = Professor.STATUS
    ZONAS = Endereco.TIPOS_ZONAS
    escola = Escola.objects.get(id=request.session['Escola'])
    erros = []
    bloqueio = False
    lecionas = Leciona.objects.filter(Professor=professor_obj, Escola=escola.id)

    if len(lecionas) > 0:
        erros.append(
            'Não foi possível apagar o professor pois ele tem referência com uma disciplina em turmas.'
        )
        bloqueio = True    

    if request.method == 'GET':
        context = {
            'erros': erros,
            'bloqueio': bloqueio,
            'Tipo_Sexo': TIPO_SEXO,
            'Tipo_Titulos': TIPOS_TITULOS,
            'Tipo_Status': STATUS,
            'zonas': ZONAS,
            'professor_dados': professor_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'usuario_dados': usuario_obj,
            'Tipo_Transacao': 'DEL',
            'idProfessor': id
        }
        return render(request,'gestaoEscolar/professor/professor_form.html', context)
    else:
        try:
            with transaction.atomic():
                professor_obj.delete()
                endereco_obj.delete()
                telefone_obj.delete()
                usuario_obj.delete()
                return redirect('professor_listagem')
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'Tipo_Sexo': TIPO_SEXO,
                'Tipo_Titulos': TIPOS_TITULOS,
                'Tipo_Status': STATUS,
                'zonas': ZONAS,
                'bloqueio': bloqueio,
                'erros':erros, 
                'professor_dados': professor_obj,
                'endereco_dados': endereco_obj,       
                'telefone_dados': telefone_obj,
                'usuario_dados': usuario_obj,
                'Tipo_Transacao': 'DEL',
                'idProfessor': id
            }
            return render(request,'gestaoEscolar/professor/professor_form.html', context)
