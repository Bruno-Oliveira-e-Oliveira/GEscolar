from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from .forms import  EscolaForm 


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


@login_required
def escola_novo(request):
    form = EscolaForm()
    return render(request,'gestaoEscolar/escola/escola_form.html',{'form':form})