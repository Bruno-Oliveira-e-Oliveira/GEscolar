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
def serie_listagem(request):
    escola = request.session['Escola']
    series = Serie.objects.filter(Escola=escola).order_by('Nivel_Escolaridade','Numero')
    context = {'series': series}
    return render(request, 'gestaoEscolar/serie/serie_listagem.html', context)

