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
from .login import salvar_escola_pessoa_sessao

@login_required
def gestao_escolar_inicio(request):
    if request.session['Escola'] == '':
        request = salvar_escola_pessoa_sessao(request)
    print(request.session['Escola'])
    return render(request,'gestaoEscolar/inicio/gestaoescolar.html')