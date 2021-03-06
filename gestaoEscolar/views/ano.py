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
from .login import salvar_escola_pessoa_sessao

@login_required
def ano_listagem(request):
    request = salvar_escola_pessoa_sessao(request)
    checarPermObj('gestaoEscolar.view_anoletivo', request.user)
    TIPOS_SITUACAO = (
        ('Todos', 'Todos'),
        ('A','Aberto'),
        ('F','Fechado')
    )
    escola = Escola.objects.get(id=request.session['Escola'])
    try:
        situacao = request.GET['situacao']
        if situacao == 'Todos':
            anos = AnoLetivo.objects.filter(Escola=escola.id).order_by('Ano','Situacao')
        else:
            anos = AnoLetivo.objects.filter(Escola=escola.id, Situacao=situacao).order_by(
                'Ano','Situacao'
            )
    except Exception as erro:
        situacao = 'Todos'
        anos = AnoLetivo.objects.filter(Escola=escola.id).order_by('Ano','Situacao')
    

    context = {'anos': anos, 'Filtro_Situacao': TIPOS_SITUACAO, 'situacao': situacao}
    return render(request, 'gestaoEscolar/ano/ano_listagem.html', context)


@login_required
def ano_novo(request):
    checarPermObj('gestaoEscolar.add_anoletivo', request.user)
    TIPOS_SITUACAO = AnoLetivo.TIPOS_SITUACAO
    if request.method == 'GET':
        context = {'Tipo_Transacao': 'INS', 'Tipos_Situacao': TIPOS_SITUACAO}
        return render(request,'gestaoEscolar/ano/ano_form.html', context)
    else:
        dados = request.POST
        escola = Escola.objects.get(id=request.session['Escola'])
        ano_dados = {
            'Ano': dados['Ano'],
            'Situacao': 'A',
            'Data_Inicio': dados['Data_Inicio'],
            'Data_Fim': dados['Data_Fim'],
            'Escola': escola.id
        }
        ano_form = AnoLetivoForm(ano_dados)
        erros_ano = {}

        if not ano_form.is_valid():
            erros_ano = ano_form.errors

        #Verifica se já existe um ano aberto
        achou = AnoLetivo.checarSituacao(escola.id)

        if erros_ano or achou:
            erros = []
            for erro in erros_ano.values():
                erros.append(erro)
            if achou:
                erro = 'Não é permitido ter dois anos letivos em aberto'
                erros.append(erro)
            context = {
                'ano_dados':ano_dados, 
                'erros':erros,  
                'Tipos_Situacao': TIPOS_SITUACAO,
                'Tipo_Transacao': 'INS'
            }
            return render(request,'gestaoEscolar/ano/ano_form.html', context)
        else:
            try:
                with transaction.atomic():
                    anoL = ano_form.save()
                    numero = Bimestre.gerar_bimestre(anoL,escola.id)
                    bimestre = Bimestre(AnoLetivo=anoL,Bimestre=numero,Escola=escola)
                    bimestre.save()
                    return redirect('ano_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'ano_dados':ano_dados, 
                    'erros':erros,  
                    'Tipos_Situacao': TIPOS_SITUACAO,
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/ano/ano_form.html', context)


@login_required
def ano_alterar(request,id):
    checarPermObj('gestaoEscolar.change_anoletivo', request.user)
    ano_obj = get_object_or_404(AnoLetivo, id=id)
    checarPermEscola(ano_obj, Escola.objects.get(id=request.session['Escola']))
    TIPOS_SITUACAO = AnoLetivo.TIPOS_SITUACAO
    escola = request.session['Escola']
    if ano_obj.Situacao == 'F':
        context = {
            'Tipos_Situacao': TIPOS_SITUACAO,
            'ano_dados': ano_obj,
            'Tipo_Transacao': 'CON',
            'idAno': id
        }
        return render(request,'gestaoEscolar/ano/ano_form.html', context)

    if request.method == 'GET':
        context = {
            'Tipos_Situacao': TIPOS_SITUACAO,
            'ano_dados': ano_obj,
            'Tipo_Transacao': 'UPD',
            'idAno': id
        }
        return render(request,'gestaoEscolar/ano/ano_form.html', context)
    else:
        dados = request.POST

        achou = False
        if ano_obj.Situacao == 'A' and dados['Situacao'] == 'F':
            achou = Bimestre.checarSituacao(escola)

        ano_dados = {
            'Ano': ano_obj.Ano,
            'Situacao': dados['Situacao'],
            'Data_Inicio': ano_obj.Data_Inicio,
            'Data_Fim': ano_obj.Data_Fim,
            'Escola': ano_obj.Escola.id
        }
        ano_form = AnoLetivoForm(ano_dados , instance=ano_obj)
        erros_ano = {}

        if not ano_form.is_valid():
            erros_ano = ano_form.errors

        if erros_ano or achou:
            erros = []
            for erro in erros_ano.values():
                erros.append(erro)
            if achou:
                erro = 'Não é possível fechar o ano pois há um bimestre em aberto.'
                erros.append(erro)
            context = {
                'Tipos_Situacao': TIPOS_SITUACAO,
                'erros':erros, 
                'ano_dados':ano_dados, 
                'Tipo_Transacao': 'UPD',
                'idAno': id
            }
            return render(request,'gestaoEscolar/ano/ano_form.html', context)
        else:
            try:
                with transaction.atomic():
                    ano = ano_form.save()


                    # TESTAR ISSO porque nao deu certo '-'
                    escola = Escola.objects.get(id=request.session['Escola'])
                    if dados['Situacao'] == 'F':
                        Matricula_Turma.mudar_situacao_alunos(ano, escola)
                    # *******************

                    return redirect('ano_listagem')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Tipos_Situacao': TIPOS_SITUACAO,
                    'erros':erros, 
                    'ano_dados':ano_dados, 
                    'Tipo_Transacao': 'UPD',
                    'idAno': id
                }
                return render(request,'gestaoEscolar/ano/ano_form.html', context)


@login_required
def ano_consultar(request,id):
    checarPermObj('gestaoEscolar.view_anoletivo', request.user)
    ano_obj = get_object_or_404(AnoLetivo, id=id)
    checarPermEscola(ano_obj, Escola.objects.get(id=request.session['Escola']))
    TIPOS_SITUACAO = AnoLetivo.TIPOS_SITUACAO
    escola = request.session['Escola']
    context = {
        'Tipos_Situacao': TIPOS_SITUACAO,
        'ano_dados': ano_obj,
        'Tipo_Transacao': 'CON',
        'idAno': id
    }
    return render(request,'gestaoEscolar/ano/ano_form.html', context)


@login_required
def ano_deletar(request,id):
    checarPermObj('gestaoEscolar.delete_anoletivo', request.user)
    ano_obj = get_object_or_404(AnoLetivo, id=id)
    checarPermEscola(ano_obj, Escola.objects.get(id=request.session['Escola']))
    TIPOS_SITUACAO = AnoLetivo.TIPOS_SITUACAO
    escola = request.session['Escola']
    erros = []
    bloqueio = False
    turmas = Turma.objects.filter(AnoLetivo=ano_obj, Escola=escola)
    bimestres = Bimestre.objects.filter(AnoLetivo=ano_obj, Escola=escola)

    if len(turmas) > 0:
        erros.append(
            'Não foi possível apagar o ano letivo pois ele tem referência com turmas.'
        )
        bloqueio = True    

    if len(bimestres) > 0:
        erros.append(
            'Não foi possível apagar o ano letivo pois ele tem referência com bimestres.'
        )
        bloqueio = True         

    if request.method == 'GET':
        context = {
            'erros': erros,
            'bloqueio': bloqueio,
            'Tipos_Situacao': TIPOS_SITUACAO,
            'ano_dados': ano_obj,
            'Tipo_Transacao': 'DEL',
            'idAno': id
        }
        return render(request,'gestaoEscolar/ano/ano_form.html', context)
    else:
        try:
            with transaction.atomic():
                ano_obj.delete()
                return redirect('ano_listagem')
        except Exception as Error:
            #Erros de servidor (500)
            print('Erro no servidor: ' + str(Error))
            Error = 'Erro no servidor'
            erros = [Error]
            context = {
                'Tipos_Situacao': TIPOS_SITUACAO,
                'bloqueio': bloqueio,
                'erros':erros, 
                'ano_dados':ano_obj, 
                'Tipo_Transacao': 'DEL',
                'idAno': id
            }
            return render(request,'gestaoEscolar/ano/ano_form.html', context)

