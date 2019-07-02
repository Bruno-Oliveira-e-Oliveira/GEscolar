from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .forms import GestorForm, EnderecoForm, TelefoneForm, EscolaForm, UsuarioForm 
from .models import Gestor, Escola, Endereco, Telefone, Pessoa, Secretaria, Professor, Aluno


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
    return render(request,'gestaoEscolar/inicio/gestaoescolar.html')


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
            'Tipo_Gestor': 'D',
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
            except Error:
                #Erros de servidor (500)
                Error = 'Erro no servidor: '+Error
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
        context = {'Niveis': NIVEIS, 'Tipos': TIPOS, 'zonas': ZONAS}
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
                'telefone_dados': telefone_dados
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
                Error = 'Erro no servidor: '+str(Error)
                erros = [Error]
                context = {
                    'Niveis': NIVEIS, 
                    'Tipos': TIPOS, 
                    'zonas': ZONAS,
                    'erros':erros, 
                    'escola_dados': escola_dados,
                    'endereco_dados': endereco_dados,       
                    'telefone_dados': telefone_dados
                }
                return render(request,'gestaoEscolar/escola/escola_form.html',context)


@login_required
def escola_alterar(request,id):
    pass