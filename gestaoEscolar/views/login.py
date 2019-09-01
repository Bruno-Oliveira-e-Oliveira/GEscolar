
from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from gestaoEscolar.forms import *
from gestaoEscolar.models import *

def login(request):
    if request.method == 'GET':
        return render(request,'gestaoEscolar/autenticacao/login_form.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            pessoa = Pessoa.obter_pessoa(usuario.username,'Pessoa')
            if pessoa.Tipo_Pessoa == 'D':
                login_auth(request, usuario)
                request = salvar_escola_pessoa_sessao(request)
                return redirect('gestao_escolar_inicio')
            else:
                if pessoa.Escola is not None:
                    if pessoa.Escola.Situacao == 'A':
                        login_auth(request, usuario)
                        request = salvar_escola_pessoa_sessao(request)
                        return redirect('gestao_escolar_inicio')
                    else:
                        erro = 'A escola está com a conta inativa.'
                        return render(request,'gestaoEscolar/autenticacao/login_form.html', {'erro':erro})    
                else:
                    erro = 'Usuário comum sem associação com uma escola, contate o administrador.'
                    return render(request,'gestaoEscolar/autenticacao/login_form.html', {'erro':erro})
        else:
            erro = 'Usuário ou senha inválidos'
            return render(request,'gestaoEscolar/autenticacao/login_form.html', {'erro':erro})


@login_required
def logout(request):
    logout_auth(request)
    return render(request,'gestaoEscolar/autenticacao/logout.html')


def salvar_escola_pessoa_sessao(request):
    pessoa = Pessoa.obter_pessoa(request.user.username,'Pessoa')
    request.session['Pessoa'] = pessoa.id
    if pessoa.Escola is not None:
        request.session['Escola'] = pessoa.Escola.id
    else:
        request.session['Escola'] = ''
        print('Sem relacionamento com uma escola')

    return request
