from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from gestaoEscolar.forms import *
from gestaoEscolar.models import *
from .permissoes import checarPermEscola, checarPermObj
 

@login_required
def leciona_listagem(request,idT):
    checarPermObj('gestaoEscolar.view_leciona', request.user)
    turma_obj = get_object_or_404(Turma, id=idT)
    checarPermEscola(turma_obj, Escola.objects.get(id=request.session['Escola']))
    escola = request.session['Escola']
    lecionas = Leciona.objects.filter(Escola=escola, Turma=turma_obj.id)
    professores = Professor.objects.filter(Escola=escola)
    disciplinas = Disciplina.objects.filter(Escola=escola).order_by('Nome')
    context = {
        'lecionas': lecionas,
        'professores': professores,
        'disciplinas': disciplinas,
        'turma': turma_obj
        }
    return render(request, 'gestaoEscolar/leciona/leciona_listagem.html', context)


@login_required
def leciona_alterar(request,idT,idL):
    checarPermObj('gestaoEscolar.change_leciona', request.user)
    turma_obj = get_object_or_404(Turma, id=idT)
    leciona_obj = get_object_or_404(Leciona, id=idL)
    checarPermEscola(turma_obj, Escola.objects.get(id=request.session['Escola']))
    checarPermEscola(leciona_obj, Escola.objects.get(id=request.session['Escola']))
    escola = request.session['Escola']
    professores = Professor.objects.filter(Escola=escola).order_by('Nome')

    if request.method == 'GET':
        context = {
            'professores': professores,
            'leciona_dados': leciona_obj,
            'Tipo_Transacao': 'UPD',
            'idL': idL,
            'idT': idT
        }
        return render(request,'gestaoEscolar/leciona/leciona_form.html', context)
    else:
        dados = request.POST

        leciona_dados = {
            'Aulas_Previstas': dados['Aulas_Previstas'],
            'Matriz_Item': leciona_obj.Matriz_Item.id,
            'Turma': leciona_obj.Turma.id,
            'Professor': dados['Professor'],
            'Escola': leciona_obj.Escola.id
        }
        leciona_form = LecionaForm(leciona_dados , instance=leciona_obj)
        erros_leciona = {}

        if not leciona_form.is_valid():
            erros_leciona = leciona_form.errors

        if erros_leciona:
            erros = []
            for erro in erros_leciona.values():
                erros.append(erro)
            context = {
                'professores': professores,
                'erros':erros, 
                'leciona_dados':leciona_dados, 
                'Tipo_Transacao': 'UPD',
                'idL': idL,
                'idT': idT
            }
            return render(request,'gestaoEscolar/leciona/leciona_form.html', context)
        else:
            try:
                with transaction.atomic():
                    leciona_form.save()
                    return redirect('leciona_listagem',idT)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'professores': professores,
                    'erros':erros, 
                    'leciona_dados':leciona_dados, 
                    'Tipo_Transacao': 'UPD',
                    'idL': idL,
                    'idT': idT
                }
                return render(request,'gestaoEscolar/leciona/leciona_form.html', context)


@login_required
def leciona_consultar(request,idT,idL):
    checarPermObj('gestaoEscolar.view_leciona', request.user)
    turma_obj = get_object_or_404(Turma, id=idT)
    leciona_obj = get_object_or_404(Leciona, id=idL)
    checarPermEscola(turma_obj, Escola.objects.get(id=request.session['Escola']))
    checarPermEscola(leciona_obj, Escola.objects.get(id=request.session['Escola']))
    escola = request.session['Escola']
    professores = Professor.objects.filter(Escola=escola).order_by('Nome')
    context = {
        'professores': professores,
        'leciona_dados': leciona_obj,
        'Tipo_Transacao': 'CON',
        'idL': idL,
        'idT': idT
    }
    return render(request,'gestaoEscolar/leciona/leciona_form.html', context)
