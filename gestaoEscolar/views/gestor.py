from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from gestaoEscolar.forms import *
from gestaoEscolar.models import *
from .permissoes import checarPermEscola, checarPermObj, checarGestor, limpar_grupos, configurar_grupos


#gestor e diretor
def diretor_novo(request):
    TIPO_SEXO = Gestor.TIPO_SEXO
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Tipo_Sexo': TIPO_SEXO, 'zonas': ZONAS,'Tipo_Transacao': 'INS'}
        return render(request,'gestaoEscolar/gestor/diretor_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'], 
            'username': dados['username'], 
            'password': dados['password'], 
            'password2': dados['password2']
        }
        gestor_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'], 
            'Usuario': '', 
            'Tipo_Pessoa': 'D',
            'Telefone': ''
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
        gestor_form = GestorForm(gestor_dados)
        usuario_form = UsuarioForm(usuario_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone_form = TelefoneForm(telefone_dados)
        erros_usuario = {}
        erros_gestor = {}
        erros_endereco = {}
        erros_telefone = {}

        if not gestor_form.is_valid():
            erros_gestor = gestor_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone1_form.errors

        if erros_usuario or erros_gestor or erros_endereco or erros_telefone:
            erros = []
            for erro in erros_gestor.values():
                erros.append(erro)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            context = {
                'Tipo_Sexo': TIPO_SEXO,
                'zonas': ZONAS,
                'erros':erros, 
                'gestor_dados':gestor_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'INS',
            }
            return render(request,'gestaoEscolar/gestor/diretor_form.html', context)
        else:
            try:
                with transaction.atomic():
                    usuario = User.objects.create_user(
                        dados['username'], 
                        dados['email'], 
                        dados['password']
                    )
                    usuario.save()
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    gestor_dados['Usuario'] = usuario.id
                    gestor_dados['Telefone'] = telefone.id
                    gestor_dados['Endereco'] = endereco.id
                    gestor_form = GestorForm(gestor_dados)
                    gestor = gestor_form.save()
                    #Configurando o grupo
                    configurar_grupos('G',usuario)
                    return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipo_Sexo': TIPO_SEXO,
                    'zonas': ZONAS,
                    'erros':erros, 
                    'gestor_dados':gestor_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'INS',
                }
                return render(request,'gestaoEscolar/gestor/diretor_form.html', context)


@login_required
def diretor_alterar(request,id):
    checarPermObj('gestaoEscolar.change_gestor', request.user)
    gestor_obj = get_object_or_404(Gestor, id=id)
    checarGestor(request.session['Pessoa'], id)
    endereco_obj = Endereco.objects.get(id=gestor_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=gestor_obj.Telefone.id)
    usuario_obj = User.objects.get(id=gestor_obj.Usuario.id)
    TIPO_SEXO = Gestor.TIPO_SEXO
    ZONAS = Endereco.TIPOS_ZONAS
    STATUS = Gestor.STATUS

    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO,
            'Tipo_Status': STATUS,
            'zonas': ZONAS,
            'gestor_dados': gestor_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'usuario_dados': usuario_obj,
            'Tipo_Transacao': 'UPD',
            'idGestor': id
        }
        return render(request,'gestaoEscolar/gestor/diretor_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'],
            'is_active': True
        }
        gestor_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'], 
            'Usuario': gestor_obj.Usuario.id, 
            'Endereco': gestor_obj.Endereco.id,
            'Tipo_Pessoa': gestor_obj.Tipo_Pessoa,
            'Telefone': gestor_obj.Telefone.id,
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
        gestor_form = GestorForm(gestor_dados , instance=gestor_obj)
        usuario_form = UsuarioEmailForm(usuario_dados, instance=usuario_obj)
        endereco_form = EnderecoForm(endereco_dados, instance=endereco_obj)
        telefone_form = TelefoneForm(telefone_dados, instance=telefone_obj)
        erros_gestor = {}
        erros_usuario = {}
        erros_endereco = {}
        erros_telefone = {}

        if not gestor_form.is_valid():
            erros_gestor = gestor_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_gestor or erros_endereco or erros_telefone or erros_usuario:
            erros = []
            for erro in erros_gestor.values():
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
                'gestor_dados':gestor_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'UPD',
                'idGestor': id
            }
            return render(request,'gestaoEscolar/gestor/diretor_form.html', context)
        else:
            try:
                with transaction.atomic():
                    usuario = usuario_form.save()
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    gestor = gestor_form.save()
                    return redirect('gestao_escolar_inicio')
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
                    'gestor_dados':gestor_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'UPD',
                    'idSecretario': id
                }
            return render(request,'gestaoEscolar/gestor/diretor_form.html', context)


def trocar_senha(request,id):
    checarPermObj('gestaoEscolar.change_gestor', request.user)
    gestor_obj = get_object_or_404(Gestor, id=id)
    checarGestor(request.session['Pessoa'], id)

    if request.method == 'GET':
        context = {
            'idGestor': id
        }
        return render(request,'gestaoEscolar/gestor/trocar_senha_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': gestor_obj.Usuario.email, 
            'username': gestor_obj.Usuario.username, 
            'password': dados['password'], 
            'password2': dados['password2']
        }
        usuario_form = UsuarioForm(usuario_dados, instance=gestor_obj.Usuario)
        erros_usuario = {}

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if erros_usuario:
            erros = []
            for erro in erros_usuario.values():
                erros.append(erro)

            context = {
                'usuario_dados': gestor_obj.Usuario,
                'erros':erros, 
                'idGestor': id
            }
            return render(request,'gestaoEscolar/gestor/trocar_senha_form.html', context)
        else:
            try:
                with transaction.atomic():
                    gestor_obj.Usuario.set_password(usuario_dados['password'])
                    gestor_obj.Usuario.save()
                    return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'usuario_dados': gestor_obj.Usuario,
                    'erros':erros, 
                    'idGestor': id
                }
                return render(request,'gestaoEscolar/gestor/trocar_senha_form.html', context)


def esqueceu_senha(request,id):
    gestor_obj = get_object_or_404(Gestor, id=id)
    
    if request.method == 'GET':
        context = {
            'idGestor': id
        }
        return render(request,'gestaoEscolar/gestor/trocar_esqueceu_senha_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': gestor_obj.Usuario.email, 
            'username': gestor_obj.Usuario.username, 
            'password': dados['password'], 
            'password2': dados['password2']
        }
        usuario_form = UsuarioForm(usuario_dados, instance=gestor_obj.Usuario)
        erros_usuario = {}

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if erros_usuario:
            erros = []
            for erro in erros_usuario.values():
                erros.append(erro)

            context = {
                'usuario_dados': gestor_obj.Usuario,
                'erros':erros, 
                'idGestor': id
            }
            return render(request,'gestaoEscolar/gestor/trocar_esqueceu_senha_form.html', context)
        else:
            try:
                with transaction.atomic():
                    gestor_obj.Usuario.set_password(usuario_dados['password'])
                    gestor_obj.Usuario.save()
                    return redirect('login')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'usuario_dados': gestor_obj.Usuario,
                    'erros':erros, 
                    'idGestor': id
                }
                return render(request,'gestaoEscolar/gestor/trocar_esqueceu_senha_form.html', context)




