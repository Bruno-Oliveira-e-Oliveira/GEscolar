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
def turma_listagem(request):
    escola = request.session['Escola']
    turmas = Turma.objects.filter(Escola=escola).order_by('Serie','Nome')
    context = {'turmas': turmas}
    return render(request, 'gestaoEscolar/turma/turma_listagem.html', context)


@login_required
def turma_novo(request):
    TIPO_PERIODO = Turma.TIPO_PERIODO
    escola = Escola.objects.get(id=request.session['Escola'])
    series = Serie.objects.filter(Escola=escola.id).order_by('Nivel_Escolaridade','Numero')
    if request.method == 'GET':
        context = {
            'Tipo_Transacao': 'INS', 
            'series': series,
            'Tipo_Periodo': TIPO_PERIODO
        }
        return render(request,'gestaoEscolar/turma/turma_form.html', context)
    else:
        dados = request.POST

        turma_dados = {
            'Nome': dados['Nome'],
            'Periodo': dados['Periodo'],
            'Sala': dados['Sala'],
            'Max_Alunos': dados['Max_Alunos'],
            'Serie': dados['Serie'],
            'Escola': escola.id
        }

        #Retorna o ano letivo ativo no momento
        ano = AnoLetivo.retornar_ativo(escola.id)  
        if ano is not None:
            turma_dados['AnoLetivo'] = ano.id

        turma_form = TurmaForm(turma_dados)
        erros_turma = {}

        if not turma_form.is_valid():
            erros_turma = turma_form.errors
        
        if erros_turma or (ano is None):
            erros = []
            for erro in erros_turma.values():
                erros.append(erro)
            if ano is None:
                erro = 'Não há nenhum ano letivo aberto no momento.'
                erros.append(erro)
            context = {
                'turma_dados':turma_dados, 
                'erros':erros,  
                'series': series,
                'Tipo_Periodo': TIPO_PERIODO, 
                'Tipo_Transacao': 'INS'
            }

            return render(request,'gestaoEscolar/turma/turma_form.html', context)
        else:
            try:
                with transaction.atomic():
                    turma = turma_form.save()
                    Leciona.gerar_lecionas(turma)
                    return redirect('turma_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'turma_dados':turma_dados, 
                    'erros':erros, 
                    'series': series, 
                    'Tipo_Periodo': TIPO_PERIODO, 
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/turma/turma_form.html', context)


@login_required
def turma_alterar(request,id):
    turma_obj = get_object_or_404(Turma, id=id)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma_obj, escola.id)
    TIPO_PERIODO = Turma.TIPO_PERIODO
    series = Serie.objects.filter(Escola=escola.id).order_by('Nivel_Escolaridade','Numero')
    ano = turma_obj.AnoLetivo.Ano
    
    if request.method == 'GET':
        turma_dados = {
            'Nome': turma_obj.Nome,
            'Periodo': turma_obj.Periodo,
            'Sala': turma_obj.Sala,
            'Max_Alunos': turma_obj.Max_Alunos,
            'Serie': turma_obj.Serie.id,
            'AnoLetivo': turma_obj.AnoLetivo.id,
            'Escola': turma_obj.Escola.id
        }
        context = {
            'turma_dados': turma_dados,
            'Tipo_Periodo': TIPO_PERIODO,
            'series': series, 
            'ano': ano,
            'Tipo_Transacao': 'UPD',
            'idTurma': id
        }
        return render(request,'gestaoEscolar/turma/turma_form.html', context)
    else:
        dados = request.POST
        turma_dados = {
            'Nome': dados['Nome'],
            'Periodo': dados['Periodo'],
            'Sala': dados['Sala'],
            'Max_Alunos': dados['Max_Alunos'],
            'Serie': turma_obj.Serie.id,
            'AnoLetivo': turma_obj.AnoLetivo.id,
            'Escola': turma_obj.Escola.id
        }
        turma_form = TurmaForm(turma_dados , instance=turma_obj)
        erros_turma = {}

        if not turma_form.is_valid():
            erros_turma = turma_form.errors

        if erros_turma:
            erros = []
            for erro in erros_turma.values():
                erros.append(erro)
            context = {
                'erros':erros, 
                'turma_dados':turma_dados, 
                'Tipo_Periodo': TIPO_PERIODO, 
                'series': series, 
                'ano': ano,
                'Tipo_Transacao': 'UPD',
                'idTurma': id
            }
            return render(request,'gestaoEscolar/turma/turma_form.html', context)
        else:
            try:
                with transaction.atomic():
                    turma_form.save()
                    return redirect('turma_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'erros':erros, 
                    'turma_dados':turma_dados, 
                    'Tipo_Periodo': TIPO_PERIODO,
                    'series': series, 
                    'ano': ano, 
                    'Tipo_Transacao': 'UPD',
                    'idturma': id
                }
                return render(request,'gestaoEscolar/turma/turma_form.html', context)


@login_required
def turma_consultar(request,id):
    turma_obj = get_object_or_404(Turma, id=id)
    TIPO_PERIODO = Turma.TIPO_PERIODO
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma_obj, escola.id)
    series = Serie.objects.filter(Escola=escola.id).order_by('Nivel_Escolaridade','Numero')

    context = {
        'turma_dados': turma_obj,
        'Tipo_Periodo': TIPO_PERIODO, 
        'series': series, 
        'Tipo_Transacao': 'CON',
        'idTurma': id
    }
    return render(request,'gestaoEscolar/turma/turma_form.html', context)


@login_required
def turma_deletar(request,id):
    turma_obj = get_object_or_404(Turma, id=id)
    TIPO_PERIODO = Turma.TIPO_PERIODO
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma_obj, escola.id)
    series = Serie.objects.filter(Escola=escola.id).order_by('Nivel_Escolaridade','Numero')

    if request.method == 'GET':
        context = {
            'turma_dados': turma_obj,
            'Tipo_Periodo': TIPO_PERIODO,
            'series': series,  
            'Tipo_Transacao': 'DEL',
            'idTurma': id
        }
        return render(request,'gestaoEscolar/turma/turma_form.html', context)
    else:
        try:
            with transaction.atomic():
                turma_obj.delete()
                return redirect('turma_listagem')
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'turma_dados': turma_obj,
                'Tipo_Periodo': TIPO_PERIODO, 
                'series': series, 
                'Tipo_Transacao': 'DEL',
                'idTurma': id
            }
            return render(request,'gestaoEscolar/turma/turma_form.html', context)


@login_required
def gerenciamento_turma_listagem(request,idT):
    turma = get_object_or_404(Turma, id=idT)
    escola = request.session['Escola']
    checarPermEscola(turma, escola)
    alunos = Aluno.objects.filter(Escola=escola).order_by('Nome')
    matriculas_ordenadas = []
    matriculas = Matricula_Turma.objects.filter(Turma=turma.id,Escola=escola)
    if len(matriculas) > 0:
        for aluno in alunos:
            for matricula in matriculas:
                if matricula.Aluno.id == aluno.id:
                    matriculas_ordenadas.append(matricula)
    context = {'matriculas': matriculas_ordenadas, 'idT': idT}
    return render(request, 'gestaoEscolar/turma/gerenciamento_turma_listagem.html', context)


@login_required
def matricula_turma_novo(request,idT):
    turma = get_object_or_404(Turma, id=idT)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma, escola.id)
    TIPOS_SITUACAO = Matricula_Turma.TIPOS_SITUACAO
    alunos = Aluno.retornar_alunos_sem_turma(escola.id)
    erros = []
    if alunos == 0:
        erros.append('Não há alunos cadastrados no sistema.')
    elif alunos == -1:
        erros.append('Não há nenhum ano letivo em aberto.')
    elif alunos == -2:
        erros.append('Não há nenhum aluno que precisa ser matriculado.')
    
    if turma.AnoLetivo.Situacao == 'F':
        erros.append('O ano letivo dessa turma já foi fechado.')

    if not turma.checarMaxAlunos():
        erros.append('O limite de alunos dessa turma já foi alcançado.')
 
    if len(erros) > 0:
        alunos = []
    
    if request.method == 'GET':
        context = {
            'erros': erros,
            'Tipo_Transacao': 'INS', 
            'alunos': alunos,
            'Tipo_Situacao': TIPOS_SITUACAO,
            'idT': idT,
            'turma': turma
        }
        return render(request,'gestaoEscolar/turma/matricula_turma_form.html', context)
    else:
        dados = request.POST

        matricula_turma_dados = {
            'Turma': turma.id ,
            'Aluno': dados['Aluno'],
            'Situacao': 'matriculado',
            'Escola': escola.id
        }

        matricula_turma_form = Matricula_Turma_Form(matricula_turma_dados)
        erros_matricula_turma = {}

        if not matricula_turma_form.is_valid():
            erros_matricula_turma = matricula_turma_form.errors
        
        if erros_matricula_turma:
            for erro in erros_matricula_turma.values():
                erros.append(erro)
            context = {
                'matricula_turma_dados':matricula_turma_dados, 
                'erros':erros,  
                'alunos': alunos,
                'Tipo_Situacao': TIPOS_SITUACAO,
                'Tipo_Transacao': 'INS',
                'idT': idT,
                'turma': turma
            }
            return render(request,'gestaoEscolar/turma/matricula_turma_form.html', context)
        else:
            try:
                with transaction.atomic():
                    matricula_turma_form.save()
                    return redirect('gerenciamento_turma_listagem',idT)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'matricula_turma_dados':matricula_turma_dados, 
                    'erros':erros,  
                    'alunos': alunos,
                    'Tipo_Situacao': TIPOS_SITUACAO,
                    'Tipo_Transacao': 'INS',
                    'idT': idT,
                    'turma': turma
                }
                return render(request,'gestaoEscolar/turma/matricula_turma_form.html', context)