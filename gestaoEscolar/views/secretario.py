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
def secretario_listagem(request):
    pessoa = Pessoa.obter_pessoa(request.user.username,'Pessoa')
    if (pessoa is not None) and (pessoa.Escola is not None):
        secretarios = Secretaria.objects.filter(Escola=pessoa.Escola).order_by('Nome')
        context = {'secretarios': secretarios}
        return render(request, 'gestaoEscolar/secretario/secretario_listagem.html', context)
    else:
        #Pessoa sem escola ou nome de usuario vazio 
        #Tratar depois
        return HttpResponse('Não foi encontrada nenhuma associação com uma escola')


@login_required
def secretario_novo(request):
    TIPO_SEXO = Secretaria.TIPO_SEXO
    STATUS = Secretaria.STATUS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Tipo_Sexo': TIPO_SEXO, 'Tipo_Status': STATUS, 'zonas': ZONAS, 'Tipo_Transacao': 'INS'}
        return render(request,'gestaoEscolar/secretario/secretario_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'],
            'is_active': dados['is_active']
        }
        secretario_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'], 
            'Usuario': '', 
            'Endereco': '',
            'Tipo_Pessoa': 'S',
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
        secretario_form = SecretarioForm(secretario_dados)
        usuario_form = UsuarioEmailForm(usuario_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone_form = TelefoneForm(telefone_dados)
        erros_secretario = {}
        erros_usuario = {}
        erros_endereco = {}
        erros_telefone = {}

        if not secretario_form.is_valid():
            erros_secretario = secretario_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone1_form.errors

        if erros_secretario or erros_endereco or erros_telefone or erros_usuario:
            erros = []
            for erro in erros_secretario.values():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)               
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            context = {
                'Tipo_Sexo': TIPO_SEXO,
                'zonas': ZONAS,
                'Tipo_Status': STATUS,
                'erros':erros, 
                'secretario_dados':secretario_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'INS'
            }
            return render(request,'gestaoEscolar/secretario/secretario_form.html', context)
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
                    secretario_dados['Usuario'] = usuario.id
                    secretario_dados['Telefone'] = telefone.id
                    secretario_dados['Endereco'] = endereco.id
                    escola = Escola.objects.get(id=request.session['Escola'])
                    secretario_dados['Escola'] = escola.id
                    secretario_form = SecretarioForm(secretario_dados)
                    secretario = secretario_form.save()
                    return redirect('secretario_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipo_Sexo': TIPO_SEXO,
                    'Tipo_Status': STATUS,
                    'zonas': ZONAS,
                    'erros':erros, 
                    'secretario_dados':secretario_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/secretario/secretario_form.html', context)


@login_required
def secretario_alterar(request,id):
    secretario_obj = Secretaria.objects.get(id=id)
    endereco_obj = Endereco.objects.get(id=secretario_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=secretario_obj.Telefone.id)
    usuario_obj = User.objects.get(id=secretario_obj.Usuario.id)
    TIPO_SEXO = Secretaria.TIPO_SEXO
    STATUS = Secretaria.STATUS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO,
            'Tipo_Status': STATUS,
            'zonas': ZONAS,
            'secretario_dados': secretario_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'usuario_dados': usuario_obj,
            'Tipo_Transacao': 'UPD',
            'idSecretario': id
        }
        return render(request,'gestaoEscolar/secretario/secretario_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'],
            'is_active': dados['is_active']
        }
        secretario_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'], 
            'Usuario': secretario_obj.Usuario.id, 
            'Endereco': secretario_obj.Endereco.id,
            'Tipo_Pessoa': secretario_obj.Tipo_Pessoa,
            'Telefone': secretario_obj.Telefone.id,
            'Escola': secretario_obj.Escola.id
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
        secretario_form = SecretarioForm(secretario_dados , instance=secretario_obj)
        usuario_form = UsuarioEmailForm(usuario_dados, instance=usuario_obj)
        endereco_form = EnderecoForm(endereco_dados, instance=endereco_obj)
        telefone_form = TelefoneForm(telefone_dados, instance=telefone_obj)
        erros_secretario = {}
        erros_usuario = {}
        erros_endereco = {}
        erros_telefone = {}

        if not secretario_form.is_valid():
            erros_secretario = secretario_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_secretario or erros_endereco or erros_telefone or erros_usuario:
            erros = []
            for erro in erros_secretario.values():
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
                'zonas': ZONAS,
                'erros':erros, 
                'secretario_dados':secretario_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'UPD',
                'idSecretario': id
            }
            return render(request,'gestaoEscolar/secretario/secretario_form.html', context)
        else:
            try:
                with transaction.atomic():
                    usuario = usuario_form.save()
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    secretario = secretario_form.save()
                    return redirect('secretario_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipo_Sexo': TIPO_SEXO,
                    'Tipo_Status': STATUS,
                    'zonas': ZONAS,
                    'erros':erros, 
                    'secretario_dados':secretario_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'UPD',
                    'idSecretario': id
                }
                return render(request,'gestaoEscolar/secretario/secretario_form.html', context)


@login_required
def secretario_consultar(request,id):
    secretario_obj = Secretaria.objects.get(id=id)
    endereco_obj = Endereco.objects.get(id=secretario_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=secretario_obj.Telefone.id)
    usuario_obj = User.objects.get(id=secretario_obj.Usuario.id)
    TIPO_SEXO = Secretaria.TIPO_SEXO
    STATUS = Secretaria.STATUS
    ZONAS = Endereco.TIPOS_ZONAS
    context = {
        'Tipo_Sexo': TIPO_SEXO,
        'zonas': ZONAS,
        'Tipo_Status': STATUS,
        'secretario_dados': secretario_obj,
        'endereco_dados': endereco_obj,       
        'telefone_dados': telefone_obj,
        'usuario_dados': usuario_obj,
        'Tipo_Transacao': 'CON',
        'idSecretario': id
    }
    return render(request,'gestaoEscolar/secretario/secretario_form.html', context)


@login_required
def secretario_deletar(request,id):
    secretario_obj = Secretaria.objects.get(id=id)
    endereco_obj = Endereco.objects.get(id=secretario_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=secretario_obj.Telefone.id)
    usuario_obj = User.objects.get(id=secretario_obj.Usuario.id)
    TIPO_SEXO = Secretaria.TIPO_SEXO
    STATUS = Secretaria.STATUS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO,
            'Tipo_Status': STATUS,
            'zonas': ZONAS,
            'secretario_dados': secretario_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'usuario_dados': usuario_obj,
            'Tipo_Transacao': 'DEL',
            'idSecretario': id
        }
        return render(request,'gestaoEscolar/secretario/secretario_form.html', context)
    else:
        try:
            with transaction.atomic():
                secretario_obj.delete()
                endereco_obj.delete()
                telefone_obj.delete()
                usuario_obj.delete()
                return redirect('secretario_listagem')
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'Tipo_Sexo': TIPO_SEXO,
                'Tipo_Status': STATUS,
                'zonas': ZONAS,
                'erros':erros, 
                'secretario_dados': secretario_obj,
                'endereco_dados': endereco_obj,       
                'telefone_dados': telefone_obj,
                'usuario_dados': usuario_obj,
                'Tipo_Transacao': 'DEL',
                'idSecretario': id
            }
            return render(request,'gestaoEscolar/secretario/secretario_form.html', context)
