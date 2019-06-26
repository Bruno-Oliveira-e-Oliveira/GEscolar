from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .forms import GestorForm, EscolaForm, UsuarioForm 


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
    if request.method == 'GET':
        return render(request,'gestaoEscolar/gestor/diretor_form.html')
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
            'Tipo_Gestor': 'D'
        }

        gestor_form = GestorForm(gestor_dados)
        usuario_form = UsuarioForm(usuario_dados)
        erros_usuario = {}
        erros_gestor = {}

        if not gestor_form.is_valid():
            erros_gestor = gestor_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if erros_usuario or erros_gestor:
            erros = []
            for chave, erro in erros_gestor.items():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)
            context = {'erros':erros, 'gestor_dados':gestor_dados, 'usuario_dados': usuario_dados }
            return render(request,'gestaoEscolar/gestor/diretor_form.html', context)
        else:
            usuario = User.objects.create_user(dados['username'], dados['email'], dados['password'])
            usuario.save()
            gestor_dados['Usuario'] = usuario.id
            gestor_form = GestorForm(gestor_dados)
            gestor_form.save()
            return redirect('gestao_escolar_inicio')


@login_required
def escola_novo(request):
    form = EscolaForm()
    return render(request,'gestaoEscolar/escola/escola_form.html',{'form':form})