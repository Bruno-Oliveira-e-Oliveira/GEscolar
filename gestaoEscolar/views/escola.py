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
def escola_novo(request):
    NIVEIS = Escola.NIVEIS_DE_ESCOLARIDADE
    TIPOS = Escola.TIPOS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Niveis': NIVEIS, 'Tipos': TIPOS, 'zonas': ZONAS,'Tipo_Transacao': 'INS'}
        return render(request,'gestaoEscolar/escola/escola_form.html',context)
    else:
        dados = request.POST
        escola_dados = {
            'Nome': dados['Nome'], 
            'Email': dados['Email'], 
            'Nivel_Escolaridade': dados['Nivel_Escolaridade'], 
            'Tipo_Escola': dados['Tipo_Escola'], 
            'Nota_de_Corte': dados['Nota_de_Corte'], 
            'Situacao': 'A',
            'Diretor': '',
            'Endereco': '',
            'Telefone': ''
        }
        endereco_dados = {
            'Rua': dados['Rua'], 
            'Numero': dados['Numero'], 
            'Bairro': dados['Bairro'], 
            'Cidade': dados['Cidade'], 
            'Estado': dados['Estado'], 
            'Complemento': dados['Complemento'],
            'Zona': dados['Zona']
        }
        telefone_dados = {
            'Numero1': dados['Numero1'], 
            'Numero2': dados['Numero2']
        }
        escola_form = EscolaForm(escola_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone_form = TelefoneForm(telefone_dados)
        erros_escola = {}
        erros_endereco = {}
        erros_telefone = {}

        if not escola_form.is_valid():
            erros_escola = escola_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_escola or erros_endereco or erros_telefone:
            erros = []
            for erro in erros_escola.values():
                erros.append(erro)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)
            context = {
                'Niveis': NIVEIS, 
                'Tipos': TIPOS, 
                'zonas': ZONAS,
                'erros':erros, 
                'escola_dados': escola_dados,
                'endereco_dados': endereco_dados,       
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'INS'
            }
            return render(request,'gestaoEscolar/escola/escola_form.html',context)
        else:
            try:
                with transaction.atomic():
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    escola_dados['Endereco'] = endereco.id
                    diretor = Pessoa.obter_pessoa(request.user.username,'Gestor')
                    escola_dados['Diretor'] = diretor.id
                    escola_dados['Telefone'] = telefone.id
                    escola_form = EscolaForm(escola_dados)
                    escola = escola_form.save()
                    diretor.tornar_diretor(escola,0) 
                    Serie.gerar_series(escola.Nivel_Escolaridade, escola)
                    return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'Niveis': NIVEIS, 
                    'Tipos': TIPOS, 
                    'zonas': ZONAS,
                    'erros':erros, 
                    'escola_dados': escola_dados,
                    'endereco_dados': endereco_dados,       
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'INS'
                }
                return render(request,'gestaoEscolar/escola/escola_form.html',context)


@login_required
def escola_alterar(request,id):
    escola_obj = get_object_or_404(Escola, id=id)
    endereco_obj = Endereco.objects.get(id=escola_obj.Endereco.id)
    telefone_obj = Telefone.objects.get(id=escola_obj.Telefone.id)
    NIVEIS = Escola.NIVEIS_DE_ESCOLARIDADE
    TIPOS = Escola.TIPOS
    ZONAS = Endereco.TIPOS_ZONAS
    STATUS = Escola.STATUS
    if request.method == 'GET':
        context = {
            'STATUS': STATUS,
            'Niveis': NIVEIS, 
            'Tipos': TIPOS, 
            'zonas': ZONAS, 
            'escola_dados': escola_obj,
            'endereco_dados': endereco_obj,       
            'telefone_dados': telefone_obj,
            'Tipo_Transacao': 'UPD',
            'idEscola': id
        }
        return render(request,'gestaoEscolar/escola/escola_form.html',context)
    else:
        dados = request.POST
        escola_dados = {
            'Nome': dados['Nome'], 
            'Email': dados['Email'], 
            'Nivel_Escolaridade': escola_obj.Nivel_Escolaridade,
            'Tipo_Escola': dados['Tipo_Escola'], 
            'Nota_de_Corte': dados['Nota_de_Corte'], 
            'Situacao': dados['Situacao'],
            'Diretor': escola_obj.Diretor.id,
            'Endereco': escola_obj.Endereco.id,
            'Telefone': escola_obj.Telefone.id
        }
        endereco_dados = {
            'Rua': dados['Rua'], 
            'Numero': dados['Numero'], 
            'Bairro': dados['Bairro'], 
            'Cidade': dados['Cidade'], 
            'Estado': dados['Estado'], 
            'Complemento': dados['Complemento'],
            'Zona': dados['Zona']
        }
        telefone_dados = {
            'Numero1': dados['Numero1'], 
            'Numero2': dados['Numero2']
        }
        escola_form = EscolaForm(escola_dados, instance=escola_obj)
        endereco_form = EnderecoForm(endereco_dados, instance=endereco_obj)
        telefone_form = TelefoneForm(telefone_dados, instance=telefone_obj)
        erros_escola = {}
        erros_endereco = {}
        erros_telefone = {}

        if not escola_form.is_valid():
            erros_escola = escola_form.errors
        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors
        if not telefone_form.is_valid():
            erros_telefone = telefone_form.errors

        if erros_escola or erros_endereco or erros_telefone:
            erros = []
            for erro in erros_escola.values():
                erros.append(erro)
                print(erros_escola)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone.values():
                erros.append(erro)

            context = {
                'STATUS': STATUS,
                'Niveis': NIVEIS, 
                'Tipos': TIPOS, 
                'zonas': ZONAS,
                'erros':erros, 
                'escola_dados': escola_dados,
                'endereco_dados': endereco_dados,       
                'telefone_dados': telefone_dados,
                'Tipo_Transacao': 'UPD',
                'idEscola': id                
            }
            return render(request,'gestaoEscolar/escola/escola_form.html',context)
        else:
            try:
                with transaction.atomic():
                    endereco = endereco_form.save()
                    telefone = telefone_form.save()
                    escola = escola_form.save()
                    if escola_dados['Situacao'] == 'I':
                        logout_auth(request)
                        return render(request,'gestaoEscolar/autenticacao/logout.html')
                    else:
                        return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                print('Erro no servidor: ' + str(Error))
                Error = 'Erro no servidor'
                erros = [Error]
                context = {
                    'STATUS': STATUS,
                    'Niveis': NIVEIS, 
                    'Tipos': TIPOS, 
                    'zonas': ZONAS,
                    'erros':erros, 
                    'escola_dados': escola_dados,
                    'endereco_dados': endereco_dados,       
                    'telefone_dados': telefone_dados,
                    'Tipo_Transacao': 'UPD',
                    'idEscola': id
                }
                return render(request,'gestaoEscolar/escola/escola_form.html',context)