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

@login_required
def boletim_aluno(request,id,tipo,idM):
    aluno = get_object_or_404(Aluno, id=id)
    matricula = get_object_or_404(Matricula_Turma, id=idM)
    if (tipo != 'L' and tipo != 'M') or (matricula.Aluno.id != aluno.id):
        raise Http404
    
    template_string = render_to_string('gestaoEscolar/relatorios/boletim.html', {'aluno': aluno})
    html = HTML(string=template_string, base_url=request.build_absolute_uri())
    main_doc = html.render()
    pdf = main_doc.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=packslip-{0}.pdf'.format('boletim')
    return response


    # context = {}
    # return render(request, 'gestaoEscolar/relatorios/boletim.html', context)




@login_required
def boletim_matricula(request,idT,idM):



    context = {}
    return render(request, 'gestaoEscolar/relatorios/boletim.html', context)

