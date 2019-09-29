
from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from gestaoEscolar.forms import *
from gestaoEscolar.models import *
from django.core.mail import send_mail

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
    request.session['Tipo_Pessoa'] = pessoa.Tipo_Pessoa
    
    if pessoa.Escola is not None:
        request.session['Escola'] = pessoa.Escola.id
    else:
        request.session['Escola'] = ''
        print('Sem relacionamento com uma escola')

    return request


def esqueceu(request):
    if request.method == 'GET':
        return render(request,'gestaoEscolar/autenticacao/esqueceu.html')
    else:
        email = request.POST['email']
        usuario = User.objects.filter(email=email)
        if len(usuario) > 0:
            pessoa = Pessoa.obter_pessoa(usuario[0].username,'Pessoa')
            titulo = 'GEscolar | Esqueceu a senha'
            email_gescolar = 'gescolar.contas@gmail.com'

            if pessoa.Tipo_Pessoa == 'D':
                link = 'http://127.0.0.1:8000/gestaoEscolar/diretor/novaSenha/' + str(pessoa.id)
                assunto = 'Click no link para trocar sua senha: ' +link
            else:
                senha = pessoa.Cpf
                assunto = 'Sua senha é: ' +senha

            try:
                send_mail(
                    titulo,
                    assunto,
                    email_gescolar,
                    [email],
                    fail_silently=False,
                )
                enviado = True
                msg = 'E-mail enviado com sucesso'
            except Exception as excp:
                enviado = False
                msg = 'Não foi possível enviar o email.'
                print(excp)

        else:
            enviado = False
            msg = 'Não há nenhuma conta com esse email.'
        context = {'enviado': enviado, 'msg':msg}
        return render(request,'gestaoEscolar/autenticacao/esqueceu.html',context)



