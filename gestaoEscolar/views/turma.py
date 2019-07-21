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
    turmas = Turma.objects.filter(Escola=escola).order_by('Nome')
    context = {'turmas': turmas}
    return render(request, 'gestaoEscolar/turma/turma_listagem.html', context)


@login_required
def turma_novo(request):
    TIPO_PERIODO = Turma.TIPO_PERIODO
    if request.method == 'GET':
        context = {'Tipo_Transacao': 'INS', 'Tipo_Periodo': TIPO_PERIODO}
        return render(request,'gestaoEscolar/turma/turma_form.html', context)
    #PAREI AQUI


    
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

