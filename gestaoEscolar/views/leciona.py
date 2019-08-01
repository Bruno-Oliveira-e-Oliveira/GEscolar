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
def leciona_listagem(request,idT):
    escola = request.session['Escola']
    lecionas = Leciona.objects.filter(Escola=escola)
    professores = Professor.objects.filter(Escola=escola)
    disciplinas = Disciplina.objects.filter(Escola=escola).order_by('Nome')
    context = {
        'lecionas': lecionas,
        'professores': professores,
        'disciplinas': disciplinas,
        'idT': idT
        }
    return render(request, 'gestaoEscolar/leciona/leciona_listagem.html', context)