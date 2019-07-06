from django.shortcuts import render, redirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .forms import *
from .models import *


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'gestaoEscolar/autenticacao/login_form.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login_auth(request, usuario)
            pessoa = Pessoa.obter_pessoa(usuario.username,'Pessoa')
            if pessoa.Escola is not None:
                request.session['Escola'] = pessoa.Escola.id
            else:
                request.session['Escola'] = ''
            return redirect('gestao_escolar_inicio')
        else:
            erro = 'Usuário ou senha inválidos'
            return render(request,'gestaoEscolar/autenticacao/login_form.html', {'erro':erro})


@login_required
def logout(request):
    logout_auth(request)
    return render(request,'gestaoEscolar/autenticacao/logout.html')


@login_required
def gestao_escolar_inicio(request):
    print(request.session['Escola'])
    return render(request,'gestaoEscolar/inicio/gestaoescolar.html')

#gestor e diretor
def diretor_novo(request):
    TIPO_SEXO = Gestor.TIPO_SEXO
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Tipo_Sexo': TIPO_SEXO, 'zonas': ZONAS}
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
                'telefone_dados': telefone_dados
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
                    'telefone_dados': telefone_dados
                }
                return render(request,'gestaoEscolar/gestor/diretor_form.html', context)


@login_required
def escola_novo(request):
    NIVEIS = Escola.NIVEIS_DE_ESCOLARIDADE
    TIPOS = Escola.TIPOS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Niveis': NIVEIS, 'Tipos': TIPOS, 'zonas': ZONAS,'Tipo_Transacao': 'INS'}
        return render(request,'gestaoEscolar/escola/escola_form.html',context)
    else:
        dados = request.POST
        escola_dados = {
            'Nome': dados['Nome'], 
            'Email': dados['Email'], 
            'Nivel_Escolaridade': dados['Nivel_Escolaridade'], 
            'Tipo_Escola': dados['Tipo_Escola'], 
            'Nota_de_Corte': dados['Nota_de_Corte'], 
            'Diretor': '',
            'Endereco': '',
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
        escola_form = EscolaForm(escola_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone_form = TelefoneForm(telefone_dados)
        erros_escola = {}
        erros_endereco = {}
        erros_telefone = {}

        if not escola_form.is_valid():
            erros_escola = escola_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_escola or erros_endereco or erros_telefone:
            erros = []
            for erro in erros_escola.values():
                erros.append(erro)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            context = {
                'Niveis': NIVEIS, 
                'Tipos': TIPOS, 
                'zonas': ZONAS,
                'erros':erros, 
                'escola_dados': escola_dados,
                'endereco_dados': endereco_dados,       
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'INS'
            }
            return render(request,'gestaoEscolar/escola/escola_form.html',context)
        else:
            try:
                with transaction.atomic():
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    escola_dados['Endereco'] = endereco.id
                    diretor = Pessoa.obter_pessoa(request.user.username,'Gestor')
                    escola_dados['Diretor'] = diretor.id
                    escola_dados['Telefone'] = telefone.id
                    escola_form = EscolaForm(escola_dados)
                    escola = escola_form.save()
                    diretor.tornar_diretor(escola,0) 
                    return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Niveis': NIVEIS, 
                    'Tipos': TIPOS, 
                    'zonas': ZONAS,
                    'erros':erros, 
                    'escola_dados': escola_dados,
                    'endereco_dados': endereco_dados,       
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/escola/escola_form.html',context)


@login_required
def escola_alterar(request,id):
    escola_obj = Escola.objects.get(id=id)
    endereco_obj = Endereco.objects.get(id=escola_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=escola_obj.Telefone.id)
    NIVEIS = Escola.NIVEIS_DE_ESCOLARIDADE
    TIPOS = Escola.TIPOS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Niveis': NIVEIS, 
            'Tipos': TIPOS, 
            'zonas': ZONAS, 
            'escola_dados': escola_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'Tipo_Transacao': 'UPD',
            'idEscola': id
        }
        return render(request,'gestaoEscolar/escola/escola_form.html',context)
    else:
        dados = request.POST
        escola_dados = {
            'Nome': dados['Nome'], 
            'Email': dados['Email'], 
            'Nivel_Escolaridade': dados['Nivel_Escolaridade'], 
            'Tipo_Escola': dados['Tipo_Escola'], 
            'Nota_de_Corte': dados['Nota_de_Corte'], 
            'Diretor': escola_obj.Diretor.id,
            'Endereco': escola_obj.Endereco.id,
            'Telefone': escola_obj.Telefone.id
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
        escola_form = EscolaForm(escola_dados, instance=escola_obj)
        endereco_form = EnderecoForm(endereco_dados, instance=endereco_obj)
        telefone_form = TelefoneForm(telefone_dados, instance=telefone_obj)
        erros_escola = {}
        erros_endereco = {}
        erros_telefone = {}

        if not escola_form.is_valid():
            erros_escola = escola_form.errors
        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors
        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_escola or erros_endereco or erros_telefone:
            erros = []
            for erro in erros_escola.values():
                erros.append(erro)
                print(erros_escola)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)

            context = {
                'Niveis': NIVEIS, 
                'Tipos': TIPOS, 
                'zonas': ZONAS,
                'erros':erros, 
                'escola_dados': escola_dados,
                'endereco_dados': endereco_dados,       
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'UPD',
                'idEscola': id                
            }
            return render(request,'gestaoEscolar/escola/escola_form.html',context)
        else:
            try:
                with transaction.atomic():
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    escola = escola_form.save()
                    return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Niveis': NIVEIS, 
                    'Tipos': TIPOS, 
                    'zonas': ZONAS,
                    'erros':erros, 
                    'escola_dados': escola_dados,
                    'endereco_dados': endereco_dados,       
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'UPD',
                    'idEscola': id
                }
                return render(request,'gestaoEscolar/escola/escola_form.html',context)


@login_required
def secretario_listagem(request):
    pessoa = Pessoa.obter_pessoa(request.user.username,'Pessoa')
    if (pessoa is not None) and (pessoa.Escola is not None):
        secretarios = Secretaria.objects.filter(Escola=pessoa.Escola)
        context = {'secretarios': secretarios}
        return render(request, 'gestaoEscolar/secretario/secretario_listagem.html', context)
    else:
        #Pessoa sem escola ou nome de usuario vazio 
        #Tratar depois
        return HttpResponse('Não foi encontrada nenhuma associação com uma escola')


@login_required
def secretario_novo(request):
    TIPO_SEXO = Secretaria.TIPO_SEXO
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Tipo_Sexo': TIPO_SEXO, 'zonas': ZONAS, 'Tipo_Transacao': 'INS'}
        return render(request,'gestaoEscolar/secretario/secretario_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email']
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
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {
            'Tipo_Sexo': TIPO_SEXO,
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
            'email': dados['email']
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