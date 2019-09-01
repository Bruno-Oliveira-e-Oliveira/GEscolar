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
def matriz_item_listagem(request,id):
    serie = get_object_or_404(Serie, id=id)
    escola = request.session['Escola']
    checarPermEscola(serie, escola)
    matriz_itens = Matriz_Item.objects.filter(Serie=serie.id,Escola=escola).order_by('Disciplina')
    context = {'matriz_itens': matriz_itens, 'serie': serie}
    return render(request, 'gestaoEscolar/serie/matriz_item_listagem.html', context)


@login_required
def matriz_item_novo(request,idS):
    escola = Escola.objects.get(id=request.session['Escola'])
    disciplinas = Disciplina.objects.filter(Escola=escola.id).order_by('Nome')
    serie = get_object_or_404(Serie, id=idS)
    checarPermEscola(serie, escola.id)
    if request.method == 'GET':
        context = {'disciplinas': disciplinas, 'Tipo_Transacao': 'INS', 'serie': serie, 'idSerie': idS}
        return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)
    else:
        dados = request.POST
        matriz_item_dados = {
            'Serie': serie.id,
            'Disciplina': dados['Disciplina'],
            'Carga': dados['Carga'],
            'Escola': escola.id
        }
        matriz_item_form = Matriz_Item_Form(matriz_item_dados)
        erros_matriz_item = {}

        if not matriz_item_form.is_valid():
            erros_matriz_item = matriz_item_form.errors

        if erros_matriz_item:
            erros = []
            for erro in erros_matriz_item.values():
                erros.append(erro)
            context = {
                'matriz_item_dados':matriz_item_dados, 
                'erros':erros,  
                'disciplinas': disciplinas,
                'serie': serie,
                'Tipo_Transacao': 'INS',
                'idSerie': idS
            }
            return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)
        else:
            try:
                with transaction.atomic():
                    item = matriz_item_form.save()
                    Leciona.atualizar_lecionas_turma('INS', item, escola.id)
                    return redirect('matriz_item_listagem', idS)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'matriz_item_dados':matriz_item_dados, 
                    'erros':erros,  
                    'disciplinas': disciplinas,
                    'serie': serie,
                    'Tipo_Transacao': 'INS',
                    'idSerie': idS
                }
                return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)


@login_required
def matriz_item_alterar(request,idS,idM):
    serie = get_object_or_404(Serie, id=idS)
    matriz_item_obj = get_object_or_404(Matriz_Item, id=idM, Serie=serie.id)
    escola = request.session['Escola']
    checarPermEscola(serie, escola)
    checarPermEscola(matriz_item_obj, escola)
    disciplinas = Disciplina.objects.filter(Escola=escola).order_by('Nome')
    if request.method == 'GET':
        context = {
            'matriz_item_dados': matriz_item_obj,
            'disciplinas': disciplinas,
            'Tipo_Transacao': 'UPD',
            'idMatriz_Item': idM,
            'idSerie': idS
        }
        return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)
    else:
        dados = request.POST
        matriz_item_dados = {
            'Serie': matriz_item_obj.Serie.id,
            'Disciplina': dados['Disciplina'],
            'Carga': dados['Carga'],
            'Escola': escola
        }
        matriz_item_form = Matriz_Item_Form(matriz_item_dados, instance=matriz_item_obj)
        erros_matriz_item = {}

        if not matriz_item_form.is_valid():
            erros_matriz_item = matriz_item_form.errors

        if erros_matriz_item:
            erros = []
            for erro in erros_matriz_item.values():
                erros.append(erro)
            context = {
                'erros':erros, 
                'matriz_item_dados':matriz_item_dados,
                'disciplinas': disciplinas, 
                'Tipo_Transacao': 'UPD',
                'idMatriz_Item': idM,
                'idSerie': idS
            }
            return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)
        else:
            try:
                with transaction.atomic():
                    matriz_item_form.save()
                    return redirect('matriz_item_listagem', idS)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'erros':erros, 
                    'matriz_item_dados':matriz_item_dados,
                    'disciplinas': disciplinas, 
                    'Tipo_Transacao': 'UPD',
                    'idMatriz_Item': idM,
                    'idSerie': idS
                }
                return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)


@login_required
def matriz_item_consultar(request,idS,idM):
    serie = get_object_or_404(Serie, id=idS)
    matriz_item_obj = get_object_or_404(Matriz_Item, id=idM, Serie=serie.id)
    escola = request.session['Escola']
    checarPermEscola(serie, escola)
    checarPermEscola(matriz_item_obj, escola)
    disciplinas = Disciplina.objects.filter(Escola=escola).order_by('Nome')
    context = {
        'matriz_item_dados':matriz_item_obj,
        'disciplinas': disciplinas, 
        'Tipo_Transacao': 'CON',
        'idMatriz_Item': idM,
        'idSerie': idS
    }
    return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)


@login_required
def matriz_item_deletar(request,idS,idM):
    serie = get_object_or_404(Serie, id=idS)
    matriz_item_obj = get_object_or_404(Matriz_Item, id=idM, Serie=serie.id)
    escola = request.session['Escola']
    checarPermEscola(serie, escola)
    checarPermEscola(matriz_item_obj, escola)
    disciplinas = Disciplina.objects.filter(Escola=escola).order_by('Nome')

    erros = []
    bloqueio = False
    achou = False
    turmas = Turma.objects.filter(Escola=escola, Serie=serie.id)
    for turma in turmas:
        if turma.AnoLetivo.Situacao == 'F':
            achou = Leciona.objects.filter(
                Matriz_Item=matriz_item_obj.id, 
                Turma=turma.id
            ).exists()
    if achou:
        erros.append(
            'Não é possível apagar o item da matriz pois ele tem referência em turmas fechadas.'
        )
        bloqueio = True
    
    if request.method == 'GET':
        context = {
            'matriz_item_dados':matriz_item_obj,
            'disciplinas': disciplinas, 
            'Tipo_Transacao': 'DEL',
            'idMatriz_Item': idM,
            'idSerie': idS,
            'erros': erros,
            'bloqueio': bloqueio
        }
        return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)
    else:
        try:
            with transaction.atomic():
                Leciona.atualizar_lecionas_turma('DEL', matriz_item_obj, escola)
                matriz_item_obj.delete()
                return redirect('matriz_item_listagem', idS)
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'matriz_item_dados':matriz_item_obj,
                'disciplinas': disciplinas, 
                'Tipo_Transacao': 'DEL',
                'idMatriz_Item': idM,
                'idSerie': idS,
                'erros':erros,
                'bloqueio': bloqueio
                }
            return render(request,'gestaoEscolar/serie/matriz_item_form.html', context)

