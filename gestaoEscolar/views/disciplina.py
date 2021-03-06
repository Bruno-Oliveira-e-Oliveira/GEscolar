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
def disciplina_listagem(request):
    checarPermObj('gestaoEscolar.view_disciplina', request.user)
    escola = request.session['Escola']
    disciplinas = Disciplina.objects.filter(Escola=escola).order_by('Nome')
    context = {'disciplinas': disciplinas}
    return render(request, 'gestaoEscolar/disciplina/disciplina_listagem.html', context)


@login_required
def disciplina_novo(request):
    checarPermObj('gestaoEscolar.add_disciplina', request.user)
    if request.method == 'GET':
        context = {'Tipo_Transacao': 'INS'}
        return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)
    else:
        dados = request.POST
        escola = Escola.objects.get(id=request.session['Escola'])
        disciplina_dados = {
            'Nome': dados['Nome'],
            'Escola': escola.id
        }
        disciplina_form = DisciplinaForm(disciplina_dados)
        erros_disciplina = {}

        if not disciplina_form.is_valid():
            erros_disciplina = disciplina_form.errors

        if erros_disciplina:
            erros = []
            for erro in erros_disciplina.values():
                erros.append(erro)
            context = {
                'disciplina_dados':disciplina_dados, 
                'erros':erros,  
                'Tipo_Transacao': 'INS'
            }
            return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)
        else:
            try:
                with transaction.atomic():
                    disciplina_form.save()
                    return redirect('disciplina_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'disciplina_dados':disciplina_dados, 
                    'erros':erros,  
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)


@login_required
def disciplina_alterar(request,id):
    checarPermObj('gestaoEscolar.change_disciplina', request.user)
    disciplina_obj = get_object_or_404(Disciplina, id=id)
    checarPermEscola(disciplina_obj, Escola.objects.get(id=request.session['Escola']))
    escola = request.session['Escola']

    if request.method == 'GET':
        context = {
            'disciplina_dados': disciplina_obj,
            'Tipo_Transacao': 'UPD',
            'idDisciplina': id
        }
        return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)
    else:
        dados = request.POST
        disciplina_dados = {
            'Nome': dados['Nome'],
            'Escola': disciplina_obj.Escola.id
        }
        disciplina_form = DisciplinaForm(disciplina_dados , instance=disciplina_obj)
        erros_disciplina = {}

        if not disciplina_form.is_valid():
            erros_disciplina = disciplina_form.errors

        if erros_disciplina:
            erros = []
            for erro in erros_disciplina.values():
                erros.append(erro)
            context = {
                'erros':erros, 
                'disciplina_dados':disciplina_dados, 
                'Tipo_Transacao': 'UPD',
                'idDisciplina': id
            }
            return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)
        else:
            try:
                with transaction.atomic():
                    disciplina = disciplina_form.save()
                    return redirect('disciplina_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'erros':erros, 
                    'disciplina_dados':disciplina_dados, 
                    'Tipo_Transacao': 'UPD',
                    'idDisciplina': id
                }
                return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)


@login_required
def disciplina_consultar(request,id):
    checarPermObj('gestaoEscolar.view_disciplina', request.user)
    disciplina_obj = get_object_or_404(Disciplina, id=id)
    checarPermEscola(disciplina_obj, Escola.objects.get(id=request.session['Escola']))
    escola = request.session['Escola']
    context = {
        'disciplina_dados': disciplina_obj,
        'Tipo_Transacao': 'CON',
        'idDisciplina': id
    }
    return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)


@login_required
def disciplina_deletar(request,id):
    checarPermObj('gestaoEscolar.delete_disciplina', request.user)
    disciplina_obj = get_object_or_404(Disciplina, id=id)
    checarPermEscola(disciplina_obj, Escola.objects.get(id=request.session['Escola']))
    escola = request.session['Escola']

    erros = []
    bloqueio = False
    itens = Matriz_Item.objects.filter(Escola=escola, Disciplina=disciplina_obj.id)
    if len(itens) > 0:
        erros.append(
            'Não foi possível apagar a disciplina pois ela tem referência com um item da matriz.'
        )
        bloqueio = True

    if request.method == 'GET':
        context = {
            'erros': erros,
            'bloqueio': bloqueio,
            'disciplina_dados': disciplina_obj,
            'Tipo_Transacao': 'DEL',
            'idDisciplina': id
        }
        return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)
    else:
        try:
            with transaction.atomic():
                disciplina_obj.delete()
                return redirect('disciplina_listagem')
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'erros': erros,
                'bloqueio': bloqueio,
                'disciplina_dados':disciplina_obj, 
                'Tipo_Transacao': 'DEL',
                'idDisciplina': id
            }
            return render(request,'gestaoEscolar/disciplina/disciplina_form.html', context)
