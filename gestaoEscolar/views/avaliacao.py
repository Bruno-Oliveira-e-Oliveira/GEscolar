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
from decimal import Decimal


@login_required
def avaliacao_listagem(request,idT):
    turma_obj = get_object_or_404(Turma, id=idT)
    escolaid = request.session['Escola']
    checarPermEscola(turma_obj, escolaid)
    pessoa = Pessoa.obter_pessoa(request.user.username, '')
    if pessoa.Tipo_Pessoa == 'P':
        lecionas = Leciona.objects.filter(Escola=escolaid, Turma=turma_obj.id, Professor=pessoa.id)
        if len(lecionas) >= 1:
            avaliacoes = []
            for leciona in lecionas:
                avaliacoes_filtradas = Avaliacao.objects.filter(
                    Escola=escolaid, 
                    Turma=turma_obj.id,
                    Leciona=leciona.id
                ).order_by('Data') 
                for avaliacao_filtrada in avaliacoes_filtradas:
                    avaliacoes.append(avaliacao_filtrada)
        else:
            avaliacoes = {}
    else:
        avaliacoes = Avaliacao.objects.filter(
            Escola=escolaid, 
            Turma=turma_obj.id,
        ).order_by('Data') 

    context = {
        'avaliacoes': avaliacoes,
        'turma': turma_obj
        }
    return render(request, 'gestaoEscolar/avaliacao/avaliacao_listagem.html', context)


@login_required
def avaliacao_novo(request,idT):
    turma = get_object_or_404(Turma, id=idT)
    escola = Escola.objects.get(id=request.session['Escola'])
    checarPermEscola(turma, escola.id)
    pessoa = Pessoa.obter_pessoa(request.user.username, '')
    alunos = Matricula_Turma.retornar_alunos_matriculados(turma, escola)

    if pessoa.Tipo_Pessoa == 'P':
        lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id, Professor=pessoa.id)
    else:
        lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id)

    erros = []
    bloqueio = False
    if len(alunos) == 0:
        erros.append('Não há alunos matriculados nessa turma.')
    
    if turma.AnoLetivo.Situacao == 'F':
        erros.append('O ano letivo dessa turma já foi fechado.')

    if not Bimestre.checarSituacao(escola.id):
        erros.append('Não há nenhum bimestre aberto.')

    if len(lecionas) == 0:
        erros.append('Não há nenhuma disciplina/professor configurada nessa turma.')
 
    if len(erros) > 0:
        bloqueio = True
    
    if request.method == 'GET':
        context = {
            'erros': erros,
            'Peso': 1,
            'Tipo_Transacao': 'INS', 
            'alunos': alunos,
            'lecionas': lecionas,
            'turma': turma,
            'bloqueio': bloqueio
        }
        return render(request,'gestaoEscolar/avaliacao/avaliacao_form.html', context)
    else:
        dados = request.POST

        avaliacao_dados = {
            'Nome': dados['Nome'],
            'Data': datetime.strptime(dados['Data'], '%Y-%m-%d').date(),
            'Leciona': dados['Leciona'],
            'Turma': turma.id,
            'Escola': escola.id
        }

        peso = dados['Peso']

        avaliacao_form = AvaliacaoForm(avaliacao_dados)
        erros_avaliacao = {}

        if not avaliacao_form.is_valid():
            erros_avaliacao = avaliacao_form.errors
        
        for erro in erros_avaliacao.values():
            erros.append(erro)

        bimestre = Bimestre.retornar_ativo(escola.id)

        if avaliacao_dados['Data'] < bimestre.Data_Inicio or avaliacao_dados['Data'] > bimestre.Data_Fim:
            erros.append('Data da avaliação fora do período do bimestre atual.')

        notas = []
        for aluno in alunos:
            matricula = Matricula_Turma.objects.filter(Turma=turma.id, Aluno=aluno.id, Escola=escola.id)
            nota_final = Nota_Final.objects.filter(
                AnoLetivo=bimestre.AnoLetivo.id,
                Matricula_Turma=matricula[0].id,
                Escola=escola.id
            )
            nota_bimestral = Nota_Bimestral.objects.filter(
                Nota_Final=nota_final[0].id,
                Bimestre=bimestre.id, 
                Escola=escola.id
            )

            nota_dados = {
                'Valor': 0,
                'Peso': peso,
                'Nota_Bimestral': nota_bimestral[0].id,
                'Escola': escola.id
            }
            nota_form = NotaForm(nota_dados)
            erros_nota = {}

            if not nota_form.is_valid():
                erros_nota = nota_form.errors
    
            if erros_nota:
                for erro in erros_nota.values():
                    erros.append(erro)

            if len(nota_bimestral) == 0:
                erros.append('Nota bimestral do aluno '+ aluno.Nome + ' não existe.')
            
            notas.append(nota_dados)

        if erros:
            context = {
                'erros': erros,
                'Tipo_Transacao': 'INS', 
                'avaliacao': avaliacao_dados,
                'alunos': alunos,
                'Peso': str(peso).replace(',','.'),
                'lecionas': lecionas,
                'turma': turma,
                'bloqueio': bloqueio
            }
            return render(request,'gestaoEscolar/avaliacao/avaliacao_form.html', context)
        else:
            try:
                with transaction.atomic():
                    avaliacao = avaliacao_form.save()
                    for nota in notas:
                        nota['Avaliacao'] = avaliacao.id
                        form = NotaForm(nota)
                        form.save()
                    return redirect('avaliacao_listagem',idT)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'erros': erros,
                    'Tipo_Transacao': 'INS', 
                    'avaliacao': avaliacao_dados,
                    'alunos': alunos,
                    'Peso': str(peso).replace(',','.'),
                    'lecionas': lecionas,
                    'turma': turma,
                    'bloqueio': bloqueio
                }
                return render(request,'gestaoEscolar/avaliacao/avaliacao_form.html', context)


@login_required
def avaliacao_alterar(request,idT,idAv):
    turma = get_object_or_404(Turma, id=idT)
    escola = Escola.objects.get(id=request.session['Escola'])
    avaliacao = get_object_or_404(Avaliacao, id=idAv)
    checarPermEscola(turma, escola.id)
    checarPermEscola(avaliacao, escola.id)
    pessoa = Pessoa.obter_pessoa(request.user.username, '')
    alunos = Matricula_Turma.retornar_alunos_matriculados(turma, escola)
    bimestre = Bimestre.retornar_ativo(escola.id)

    if pessoa.Tipo_Pessoa == 'P':
        lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id, Professor=pessoa.id)
    else:
        lecionas = Leciona.objects.filter(Escola=escola.id, Turma=turma.id)

    erros = []
    bloqueio = False
    
    if turma.AnoLetivo.Situacao == 'F':
        erros.append('O ano letivo dessa turma já foi fechado.')

    if not Bimestre.checarSituacao(escola.id):
        erros.append('Não há nenhum bimestre aberto.')
 
    if len(erros) > 0:
        bloqueio = True

    if request.method == 'GET':
        notas_alunos = []
        for aluno in alunos:
            nota_aluno = {}
            matricula = Matricula_Turma.objects.filter(
                Turma=turma.id, 
                Aluno=aluno.id, Escola=escola.id
            )
            nota_final = Nota_Final.objects.filter(
                AnoLetivo=bimestre.AnoLetivo.id,
                Matricula_Turma=matricula[0].id,
                Escola=escola.id
            )
            nota_bimestral = Nota_Bimestral.objects.filter(
                Nota_Final=nota_final[0].id,
                Bimestre=bimestre.id, 
                Escola=escola.id
            )
            nota = Nota.objects.filter(
                Escola=escola.id, 
                Avaliacao=avaliacao.id, 
                Nota_Bimestral=nota_bimestral[0].id
            )                

            if len(nota) > 0:
                nota_aluno['Aluno'] = aluno
                nota_aluno['Nota'] = nota[0]
                notas_alunos.append(nota_aluno)
        
        peso = notas_alunos[0]['Nota'].Peso

        context = {
            'erros': erros,
            'Tipo_Transacao': 'UPD', 
            'avaliacao_dados': avaliacao,
            'notas_alunos': notas_alunos,
            'Peso': str(peso).replace(',','.'),
            'lecionas': lecionas,
            'turma': turma,
            'bloqueio': bloqueio,
            'idAv': idAv
        }
        return render(request,'gestaoEscolar/avaliacao/avaliacao_form.html', context)
    else:
        dados = request.POST

        avaliacao_dados = {
            'Nome': dados['Nome'],
            'Data': datetime.strptime(dados['Data'], '%Y-%m-%d').date(),
            'Leciona': avaliacao.Leciona.id,
            'Turma': avaliacao.Turma.id,
            'Escola': escola.id
        }

        peso = dados['Peso']

        avaliacao_form = AvaliacaoForm(avaliacao_dados , instance=avaliacao)
        erros_avaliacao = {}

        if not avaliacao_form.is_valid():
            erros_avaliacao = avaliacao_form.errors

        if avaliacao_dados['Data'] < bimestre.Data_Inicio or avaliacao_dados['Data'] > bimestre.Data_Fim:
            erros.append('Data da avaliação fora do período do bimestre atual.')

        forms = []
        notas_alunos = []
        for aluno in alunos:
            nota_aluno = {}
            matricula = Matricula_Turma.objects.filter(
                Turma=turma.id, 
                Aluno=aluno.id, Escola=escola.id
            )
            nota_final = Nota_Final.objects.filter(
                AnoLetivo=bimestre.AnoLetivo.id,
                Matricula_Turma=matricula[0].id,
                Escola=escola.id
            )
            nota_bimestral = Nota_Bimestral.objects.filter(
                Nota_Final=nota_final[0].id,
                Bimestre=bimestre.id, 
                Escola=escola.id
            )
            nota = Nota.objects.filter(
                Escola=escola.id, 
                Avaliacao=avaliacao.id, 
                Nota_Bimestral=nota_bimestral[0].id
            )

            chave_nota = 'Nota-'
            chave_nota += str(aluno.id)
            valor = dados[chave_nota]

            nota_dados = {
                'Valor': str(valor).replace(',','.'),
                'Peso': peso,
                'Avaliacao': nota[0].Avaliacao.id,
                'Nota_Bimestral': nota[0].Nota_Bimestral.id,
                'Escola': escola.id
            }
            nota_form = NotaForm(nota_dados, instance=nota[0])
            erros_nota = {}

            if not nota_form.is_valid():
                erros_nota = nota_form.errors
    
            if erros_nota:
                for erro in erros_nota.values():
                    erros.append(erro)
            
            nota_aluno['Aluno'] = aluno
            nota_aluno['Nota'] = nota_dados
            notas_alunos.append(nota_aluno)
            forms.append(nota_form)

        if erros_avaliacao:
            for erro in erros_avaliacao.values():
                erros.append(erro)
            context = {
                'erros': erros,
                'Tipo_Transacao': 'UPD', 
                'avaliacao_dados': avaliacao_dados,
                'notas_alunos': notas_alunos,
                'Peso': str(peso).replace(',','.'),
                'lecionas': lecionas,
                'turma': turma,
                'bloqueio': bloqueio,
                'idAv': idAv
            }
            return render(request,'gestaoEscolar/avaliacao/avaliacao_form.html', context)
        else:
            try:
                with transaction.atomic():
                    avaliacao = avaliacao_form.save()
                    for form in forms:
                        form.save()                    
                    return redirect('avaliacao_listagem',idT)
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'erros': erros,
                    'Tipo_Transacao': 'UPD', 
                    'avaliacao_dados': avaliacao_dados,
                    'notas_alunos': notas_alunos,
                    'Peso': str(peso).replace(',','.'),
                    'lecionas': lecionas,
                    'turma': turma,
                    'bloqueio': bloqueio,
                    'idAv': idAv
                }
                return render(request,'gestaoEscolar/avaliacao/avaliacao_form.html', context)






