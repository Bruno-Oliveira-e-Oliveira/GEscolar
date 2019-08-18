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