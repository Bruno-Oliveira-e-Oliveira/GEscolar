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
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML
from gescolar import settings
import datetime

@login_required
def boletim_aluno(request,id,tipo,idM):
    aluno = get_object_or_404(Aluno, id=id)
    matricula = get_object_or_404(Matricula_Turma, id=idM)
    if (tipo != 'L' and tipo != 'M') or (matricula.Aluno.id != aluno.id):
        raise Http404
    return gerar_boletim(request,matricula)


@login_required
def boletim_matricula(request,idT,idM):
    turma = get_object_or_404(Turma, id=idT)
    matricula = get_object_or_404(Matricula_Turma, id=idM)
    return gerar_boletim(request,matricula)


def gerar_boletim(request,matricula):
    matricula_aluno = Matricula.objects.get(Aluno=matricula.Aluno.id)
    itens = Matriz_Item.objects.filter(Serie=matricula.Turma.Serie.id)
    disciplinas = Disciplina.objects.all().order_by('Nome')
    bimestres = Bimestre.objects.filter(AnoLetivo=matricula.Turma.AnoLetivo.id).order_by('Bimestre')
    notas_finais = Nota_Final.objects.filter(Matricula_Turma=matricula.id, AnoLetivo=matricula.Turma.AnoLetivo.id)
    matriz_dados = []
    ultimo_bimestre = None

    for disciplina in disciplinas:
        linha = {}
        dados_notas = []
        for item in itens:
            if disciplina.id == item.Disciplina.id:
                linha['Disciplina'] = disciplina.Nome
                for nota_final in notas_finais:
                    if nota_final.Leciona.Matriz_Item.Disciplina.id == disciplina.id:
                        notas_bimestrais = Nota_Bimestral.objects.filter(Nota_Final=nota_final.id)
                        for bimestre in bimestres:
                            for nota_bimestral in notas_bimestrais:
                                if bimestre.id == nota_bimestral.Bimestre.id:
                                    dados_notas.append(nota_bimestral.Media)
                            ultimo_bimestre = bimestre
                        linha['Medias'] = dados_notas
                        linha['Final'] = nota_final.Media_Final
                matriz_dados.append(linha)

    now = datetime.datetime.now()
    if ultimo_bimestre is not None:
        if ultimo_bimestre.Situacao == 'A':
            obs = str(ultimo_bimestre.Bimestre) + 'º Bimestre está em aberto.'
        else:
            obs = str(ultimo_bimestre.Bimestre) + 'º Bimestre já está fechado.'
    else: 
        obs = None

    context = {
        'matricula_aluno': matricula_aluno,
        'matricula_turma': matricula,
        'matriz_dados': matriz_dados,
        'now': now,
        'obs': obs
    }
    
    template_string = render_to_string('gestaoEscolar/relatorios/boletim.html', context)
    html = HTML(string=template_string, base_url=request.build_absolute_uri())
    main_doc = html.render()
    pdf = main_doc.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=boletim.pdf'
    return response