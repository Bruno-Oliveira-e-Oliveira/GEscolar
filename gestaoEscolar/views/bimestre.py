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
def bimestre_listagem(request,idA):
    escola = request.session['Escola']
    ano = get_object_or_404(AnoLetivo, id=idA)
    checarPermEscola(ano, escola)
    bimestres = Bimestre.objects.filter(Escola=escola,AnoLetivo=idA).order_by('Bimestre')
    #Gera o número do bimestre em sequência
    numero_bimestre = Bimestre.gerar_bimestre(ano,escola)
    context = {'bimestres': bimestres, 'numero_bimestre': numero_bimestre, 'idA': idA}
    return render(request, 'gestaoEscolar/bimestre/bimestre_listagem.html', context)


@login_required
def bimestre_novo(request,idA):
    escola = request.session['Escola']
    ano = get_object_or_404(AnoLetivo, id=idA)
    checarPermEscola(ano, escola)
    TIPOS_SITUACAO = Bimestre.TIPOS_SITUACAO
    #Gera o número do bimestre em sequência
    numero_bimestre = Bimestre.gerar_bimestre(ano,escola)

    if request.method == 'GET':
        context = {
            'Tipo_Transacao': 'INS', 
            'Tipos_Situacao': TIPOS_SITUACAO, 
            'ano':ano, 
            'numero_bimestre': numero_bimestre,
            'idA': idA
        }
        return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)
    else:
        dados = request.POST
        bimestre_dados = {
            'AnoLetivo': ano.id,
            'Bimestre': numero_bimestre,
            'Situacao': 'A',
            'Data_Inicio': dados['Data_Inicio'],
            'Data_Limite_Notas': dados['Data_Limite_Notas'],
            'Data_Fim': dados['Data_Fim'],
            'Escola': escola
        }
        bimestre_form = BimestreForm(bimestre_dados)
        erros_bimestre = {}

        if not bimestre_form.is_valid():
            erros_bimestre = bimestre_form.errors

        #Verifica se já existe um bimestre em aberto
        achou = Bimestre.checarSituacao(escola)

        #Verifica se o ano letivo está aberto
        fechado = False
        if ano.Situacao == 'F':
            fechado = True

        errado = False
        inicio = datetime.strptime(bimestre_dados['Data_Inicio'], '%Y-%m-%d')
        fim = datetime.strptime(bimestre_dados['Data_Fim'], '%Y-%m-%d')
        if inicio.date() < ano.Data_Inicio or fim.date() > ano.Data_Fim:
            errado = True

        bimestre_anterior = False

        bimestres = Bimestre.objects.filter(
            Bimestre=(numero_bimestre - 1),
            AnoLetivo=ano.id, 
            Escola=ano.Escola.id
        )
        
        if len(bimestres) > 0:
            for item in bimestres:
                if item.Data_Fim >= inicio.date():
                    bimestre_anterior = True
    
        if erros_bimestre or achou or fechado or errado or bimestre_anterior:
            erros = []
            for erro in erros_bimestre.values():
                erros.append(erro)
            if achou:
                erro = 'Não é permitido ter dois bimestres em aberto.'
                erros.append(erro)
            if fechado:
                erro = 'Ano letivo está fechado.'
                erros.append(erro)
            if errado:
                erro = '''As datas inicial e final do bimestre devem estar dentro do período das datas 
                    de abertura e encerramento do ano letivo ao qual elas pertencem.'''
                erros.append(erro)
            if bimestre_anterior:
                erro = '''As datas desse bimestre devem ser depois do bimestre anterior.'''
                erros.append(erro)

            context = {
                'bimestre_dados':bimestre_dados, 
                'erros':erros,  
                'Tipos_Situacao': TIPOS_SITUACAO,
                'ano': ano,
                'Tipo_Transacao': 'INS',
                'idA': idA
            }
            return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)
        else:
            try:
                with transaction.atomic():
                    bimestre = bimestre_form.save()
                    escola = Escola.objects.get(id=request.session['Escola'])
                    valor = Nota_Bimestral.gerar_nota_bimestral_por_bimestre(bimestre, escola)
                    return redirect('bimestre_listagem',idA)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'bimestre_dados':bimestre_dados, 
                    'erros':erros,  
                    'Tipos_Situacao': TIPOS_SITUACAO,
                    'ano':ano, 
                    'Tipo_Transacao': 'INS',
                    'idA': idA
                }
                return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)

    
@login_required
def bimestre_alterar(request,idA,idB):
    escola = request.session['Escola']
    bimestre_obj = get_object_or_404(Bimestre, id=idB, Escola=escola)
    ano = get_object_or_404(AnoLetivo, id=idA)
    checarPermEscola(ano, escola)
    checarPermEscola(bimestre_obj, escola)
    TIPOS_SITUACAO = Bimestre.TIPOS_SITUACAO
    if bimestre_obj.Situacao == 'F':
        context = {
            'Tipos_Situacao': TIPOS_SITUACAO,
            'bimestre_dados': bimestre_obj,
            'ano':ano, 
            'Tipo_Transacao': 'CON',
            'idBimestre': idB,
            'idA': idA
        }
        return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)

    if request.method == 'GET':
        context = {
            'Tipos_Situacao': TIPOS_SITUACAO,
            'bimestre_dados': bimestre_obj,
            'ano':ano, 
            'Tipo_Transacao': 'UPD',
            'idBimestre': idB,
            'idA': idA
        }
        return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)
    else:
        dados = request.POST

        bimestre_dados = {
            'AnoLetivo': bimestre_obj.AnoLetivo.id,
            'Bimestre': bimestre_obj.Bimestre,
            'Situacao': dados['Situacao'],
            'Data_Inicio': dados['Data_Inicio'],
            'Data_Limite_Notas': dados['Data_Limite_Notas'],
            'Data_Fim': dados['Data_Fim'],
            'Escola': bimestre_obj.Escola.id
        }
        bimestre_form = BimestreForm(bimestre_dados , instance=bimestre_obj)
        erros_bimestre = {}

        erros = []

        if not bimestre_form.is_valid():
            erros_bimestre = bimestre_form.errors
            for erro in erros_bimestre.values():
                erros.append(erro)
        
        inicio = datetime.strptime(bimestre_dados['Data_Inicio'], '%Y-%m-%d')
        fim = datetime.strptime(bimestre_dados['Data_Fim'], '%Y-%m-%d')

        if inicio.date() < ano.Data_Inicio or fim.date() > ano.Data_Fim:
            erros.append(
                '''As datas inicial e final do bimestre devem estar dentro do período das datas de 
                abertura e encerramento do ano letivo ao qual elas pertencem.'''
            )

        bimestres = Bimestre.objects.filter(
            Bimestre=(bimestre_obj.Bimestre - 1),
            AnoLetivo=bimestre_obj.AnoLetivo.id, 
            Escola=bimestre_obj.AnoLetivo.Escola.id
        )
        
        if len(bimestres) > 0:
            for item in bimestres:
                if item.Data_Fim >= inicio.date():
                    erros.append(
                        '''As datas desse bimestre devem ser depois do bimestre anterior.'''
                    )

        if erros:
            context = {
                'Tipos_Situacao': TIPOS_SITUACAO,
                'erros':erros, 
                'bimestre_dados':bimestre_dados, 
                'ano':ano,
                'Tipo_Transacao': 'UPD',
                'idBimestre': idB,
                'idA': idA
            }
            return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)
        else:
            try:
                with transaction.atomic():
                    bimestre = bimestre_form.save()
                    if dados['Situacao'] == 'F':
                        notas = Nota_Final.objects.filter(
                            AnoLetivo=bimestre.AnoLetivo.id, 
                            Escola=escola
                        )
                        for nota in notas:
                            nota.calcular_nota_final()
                    return redirect('bimestre_listagem',idA)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipos_Situacao': TIPOS_SITUACAO,
                    'erros':erros, 
                    'bimestre_dados':bimestre_dados,
                    'ano':ano, 
                    'Tipo_Transacao': 'UPD',
                    'idBimestre': idB,
                    'idA': idA
                }
                return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)


@login_required
def bimestre_consultar(request,idA,idB):
    escola = request.session['Escola']
    bimestre_obj = get_object_or_404(Bimestre, id=idB, Escola=escola)
    ano = get_object_or_404(AnoLetivo, id=idA)
    checarPermEscola(ano, escola)
    checarPermEscola(bimestre_obj, escola)
    TIPOS_SITUACAO = Bimestre.TIPOS_SITUACAO
    context = {
        'Tipos_Situacao': TIPOS_SITUACAO,
        'bimestre_dados': bimestre_obj,
        'ano':ano, 
        'Tipo_Transacao': 'CON',
        'idBimestre': idB,
        'idA': idA
    }
    return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)


@login_required
def bimestre_deletar(request,idA,idB):
    escola = request.session['Escola']
    bimestre_obj = get_object_or_404(Bimestre, id=idB, Escola=escola)
    ano = get_object_or_404(AnoLetivo, id=idA)
    checarPermEscola(ano, escola)
    checarPermEscola(bimestre_obj, escola)
    TIPOS_SITUACAO = Bimestre.TIPOS_SITUACAO


    erros = []
    bloqueio = False
    notas = Nota_Bimestral.objects.filter(Escola=escola, Bimestre=bimestre_obj.id)
    aulas = Aula.objects.filter(Escola=escola, Bimestre=bimestre_obj.id)
    if len(notas) > 0 or len(aulas) > 0:
        erros.append(
            'Não foi possível apagar o bimestre pois ele tem referência com as matrículas dos alunos.'
        )
        bloqueio = True

    if request.method == 'GET':
        context = {
            'erros': erros,
            'bloqueio': bloqueio,
            'Tipos_Situacao': TIPOS_SITUACAO,
            'bimestre_dados': bimestre_obj,
            'ano':ano, 
            'Tipo_Transacao': 'DEL',
            'idBimestre': idB,
            'idA': idA
        }
        return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)
    else:
        try:
            with transaction.atomic():
                bimestre_obj.delete()
                return redirect('bimestre_listagem',idA)
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'Tipos_Situacao': TIPOS_SITUACAO,
                'erros':erros, 
                'bloqueio': bloqueio,
                'bimestre_dados':bimestre_obj, 
                'ano':ano, 
                'Tipo_Transacao': 'DEL',
                'idBimestre': idB,
                'idA': idA
            }
            return render(request,'gestaoEscolar/bimestre/bimestre_form.html', context)

