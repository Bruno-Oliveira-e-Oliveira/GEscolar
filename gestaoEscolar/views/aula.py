from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from gestaoEscolar.forms import *
from gestaoEscolar.models import *
from .permissoes import checarPermEscola


@login_required
def aula_listagem(request):
    escola = request.session['Escola']
    turmas = Turma.objects.filter(Escola=escola)
    context = {'turmas': turmas}
    return render(request, 'gestaoEscolar/aula/aula_listagem.html', context)
    

@login_required
def aula_listagem_ajax(request):
    escola = request.session['Escola']
    turma = request.POST['turma_filtro']
    aulas = Aula.objects.filter(Escola=escola,Turma=turma).order_by('Data')
    aulas_retorno = {}
    if aulas is not None:
        for aula in aulas:
            aulas_retorno[aula.id] = {}
            aulas_retorno[aula.id]['id'] = aula.id
            aulas_retorno[aula.id]['Data'] = aula.Data
            aulas_retorno[aula.id]['Disciplina'] = aula.Leciona.Matriz_Item.Disciplina.Nome
            aulas_retorno[aula.id]['Professor'] = aula.Leciona.Professor.Nome
            aulas_retorno[aula.id]['Turma'] = aula.Turma.nome_editado
            aulas_retorno[aula.id] 
    return JsonResponse(aulas_retorno)
