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
def aula_listagem(request,idT):
    turma = get_object_or_404(Turma, id=idT)
    escola = request.session['Escola']
    checarPermEscola(turma, escola)
    aulas = Aula.objects.filter(Escola=escola, Turma=idT)
    context = {'turma': turma, 'aulas': aulas}
    return render(request, 'gestaoEscolar/aula/aula_listagem.html', context)
    

# @login_required
# def aula_listagem_ajax(request):
#     escola = request.session['Escola']
#     turma = request.POST['turma_filtro']
#     aulas = Aula.objects.filter(Escola=escola,Turma=turma).order_by('Data')
#     aulas_retorno = {}
#     if aulas is not None:
#         for aula in aulas:
#             aulas_retorno[aula.id] = {}
#             aulas_retorno[aula.id]['id'] = aula.id
#             aulas_retorno[aula.id]['Data'] = aula.Data
#             aulas_retorno[aula.id]['Disciplina'] = aula.Leciona.Matriz_Item.Disciplina.Nome
#             aulas_retorno[aula.id]['Professor'] = aula.Leciona.Professor.Nome
#             aulas_retorno[aula.id]['Turma'] = aula.Turma.nome_editado
#             aulas_retorno[aula.id] 
#     return JsonResponse(aulas_retorno)


@login_required
def aula_novo(request,idT):
    turma = get_object_or_404(Turma, id=idT)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma, escola.id)
    lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id)
    alunos = Matricula_Turma.retornar_alunos_matriculados(turma, escola)
    erros = []
    bloqueio = False

    if len(lecionas) == 0:
        erros.append('Não há registros na tabela de disciplinas x professores.')

    if len(alunos) == 0:
        erros.append('Não há nenhum aluno matriculado nessa turma.')

    if len(erros) > 0:
        bloqueio = True

    if request.method == 'GET':
        context = {
            'Tipo_Transacao': 'INS',
            'erros': erros,
            'turma': turma, 
            'lecionas': lecionas,
            'bloqueio': bloqueio
        }
        return render(request,'gestaoEscolar/aula/aula_form.html', context)
    else:
        dados = request.POST
        aula_dados = {
            'Data': dados['Data'],
            'Tema': dados['Tema'],
            'Turma': turma.id,
            'Leciona': dados['Leciona'],
            'Escola': escola.id
        }
        aula_form = AulaForm(aula_dados)
        erros_aula = {}

        if not aula_form.is_valid():
            erros_aula = aula_form.errors

        if erros_aula:
            for erro in erros_aula.values():
                erros.append(erro)
            context = {
                'aula_dados':aula_dados, 
                'erros':erros,  
                'turma': turma,      
                'lecionas': lecionas, 
                'Tipo_Transacao': 'INS',
                'bloqueio': bloqueio
            }
            return render(request,'gestaoEscolar/aula/aula_form.html', context)
        else:
            try:
                with transaction.atomic():
                    aula = aula_form.save()
                    Frequencia.gerar_frequencias(aula, escola)
                    return redirect('aula_listagem',turma.id)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'aula_dados':aula_dados, 
                    'erros':erros,  
                    'turma': turma,
                    'lecionas': lecionas, 
                    'Tipo_Transacao': 'INS',
                    'bloqueio': bloqueio
                }
                return render(request,'gestaoEscolar/aula/aula_form.html', context)


@login_required
def aula_alterar(request,idT,idA):
    turma = get_object_or_404(Turma, id=idT)
    aula_obj = get_object_or_404(Aula, id=idA)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma, escola.id)
    checarPermEscola(aula_obj, escola.id)
    lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id)
    erros = []
    bloqueio = False

    if request.method == 'GET':
        context = {
            'aula_dados': aula_obj,
            'erros':erros,  
            'lecionas': lecionas,
            'Tipo_Transacao': 'UPD',
            'turma': turma,
            'idA': idA,
            'bloqueio': bloqueio
        }
        return render(request,'gestaoEscolar/aula/aula_form.html', context)
    else:
        dados = request.POST
        aula_dados = {
            'Data': dados['Data'],
            'Tema': dados['Tema'],
            'Turma': turma.id,
            'Leciona': aula_obj.Leciona.id,
            'Escola': escola.id
        }
        aula_form = AulaForm(aula_dados, instance=aula_obj)
        erros_aula = {}

        if not aula_form.is_valid():
            erros_aula = aula_form.errors

        if erros_aula:
            erros = []
            for erro in erros_aula.values():
                erros.append(erro)
            context = {
                'aula_dados': aula_dados,
                'erros':erros,  
                'lecionas': lecionas,
                'Tipo_Transacao': 'UPD',
                'turma': turma,
                'idA': idA,
                'bloqueio': bloqueio
            }
            return render(request,'gestaoEscolar/aula/aula_form.html', context)
        else:
            try:
                with transaction.atomic():
                    aula_form.save()
                    return redirect('aula_listagem',turma.id)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'aula_dados': aula_dados,
                    'erros':erros,  
                    'lecionas': lecionas,
                    'Tipo_Transacao': 'UPD',
                    'turma': turma,
                    'idA': idA,
                    'bloqueio': bloqueio
                }
                return render(request,'gestaoEscolar/aula/aula_form.html', context)


@login_required
def aula_consultar(request,idT,idA):
    turma = get_object_or_404(Turma, id=idT)
    aula_obj = get_object_or_404(Aula, id=idA)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma, escola.id)
    checarPermEscola(aula_obj, escola.id)
    lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id)

    context = {
        'aula_dados': aula_obj,
        'lecionas': lecionas,
        'Tipo_Transacao': 'CON',
        'turma': turma,
        'idA': idA
    }
    return render(request,'gestaoEscolar/aula/aula_form.html', context)


@login_required
def aula_deletar(request,idT,idA):
    turma = get_object_or_404(Turma, id=idT)
    aula_obj = get_object_or_404(Aula, id=idA)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma, escola.id)
    checarPermEscola(aula_obj, escola.id)
    lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id)
    erros = []
    bloqueio = False

    if request.method == 'GET':
        context = {
            'aula_dados': aula_obj,
            'erros':erros,  
            'lecionas': lecionas,
            'Tipo_Transacao': 'DEL',
            'idA': idA,
            'turma': turma,
            'bloqueio': bloqueio
        }
        return render(request,'gestaoEscolar/aula/aula_form.html', context)
    else:
        try:
            with transaction.atomic():
                Frequencia.apagar_frequencias(aula_obj, escola)
                aula_obj.delete()
                return redirect('aula_listagem',turma.id)
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'aula_dados': aula_obj,
                'erros':erros,  
                'lecionas': lecionas,
                'Tipo_Transacao': 'DEL',
                'idA': idA,
                'turma': turma,
                'bloqueio': bloqueio
            }
            return render(request,'gestaoEscolar/aula/aula_form.html', context)

            
@login_required
def lista_chamada(request,idT,idA):
    turma = get_object_or_404(Turma, id=idT)
    aula_obj = get_object_or_404(Aula, id=idA)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma, escola.id)
    checarPermEscola(aula_obj, escola.id)
    frequencias = Frequencia.objects.filter(Escola=escola.id, Aula=aula_obj.id)

    if request.method == 'GET':
        context = {
            'turma': turma, 
            'aula': aula_obj,
            'frequencias': frequencias 
        }
        return render(request,'gestaoEscolar/aula/chamada_form.html', context)
    else:
        dados = request.POST
        erros = []
        forms = []

        for frequencia in frequencias:
            chave = 'Presenca'
            chave += str(frequencia.Aluno.id)

            if chave in dados:
                presenca = dados[chave]
            else:
                presenca = 'Ausente'

            chamada_dados = {
                'Presenca': presenca,
                'Aula': aula_obj.id,
                'Aluno': frequencia.Aluno.id,
                'Escola': escola.id
            }
            chamada_form = FrequenciaForm(chamada_dados, instance=frequencia)
            erros_chamada = {}

            if not chamada_form.is_valid():
                erros_chamada = chamada_form.errors
    
            if erros_chamada:
                for erro in erros_chamada.values():
                    erros.append(erro)
            
            forms.append(chamada_form)
            
        if erros:        
            context = {
                'turma': turma, 
                'aula': aula_obj,
                'frequencias': frequencias,
                'erros': erros
            }
            return render(request,'gestaoEscolar/aula/chamada_form.html', context)
        else:
            try:
                with transaction.atomic():
                    for form_chamada in forms:
                        form_chamada.save()
                    return redirect('aula_listagem',turma.id)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'turma': turma, 
                    'aula': aula_obj,
                    'frequencias': frequencias,
                    'erros': erros
                }
                return render(request,'gestaoEscolar/aula/chamada_form.html', context)

            
            
        
     



        

