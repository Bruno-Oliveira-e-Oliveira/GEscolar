from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .forms import GestorForm, EnderecoForm, TelefoneForm, EscolaForm, UsuarioForm 
from .models import Gestor, Escola, Endereco, Telefone, Pessoa, Secretaria, Professor, Aluno


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'gestaoEscolar/autenticacao/login_form.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login_auth(request, usuario)
            return redirect('gestao_escolar_inicio')
        else:
            erro = 'Usuário ou senha inválidos'
            return render(request,'gestaoEscolar/autenticacao/login_form.html', {'erro':erro})


@login_required
def logout(request):
    logout_auth(request)
    return render(request,'gestaoEscolar/autenticacao/logout.html')


@login_required
def gestao_escolar_inicio(request):
    return render(request,'gestaoEscolar/inicio/gestaoescolar.html')


def obter_pessoa(nome_usuario, tipo):
    usuario = User.objects.get(username=nome_usuario)
    if tipo == 'Gestor':
        pessoa = Gestor.objects.filter(Usuario=usuario.id)
    elif tipo == 'Secretaria':
        pessoa = Secretaria.objects.filter(Usuario=usuario.id)
    elif tipo == 'Professor':
        pessoa = Professor.objects.filter(Usuario=usuario.id)
    elif tipo == 'Aluno':
        pessoa = Aluno.objects.filter(Usuario=usuario.id)
    else:
        pessoa = Pessoa.objects.filter(Usuario=usuario.id)

    if pessoa is not None:
        return pessoa[0]
    else:
        return 0


def diretor_novo(request):
    TIPO_SEXO = Gestor.TIPO_SEXO
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Tipo_Sexo': TIPO_SEXO, 'zonas': ZONAS}
        return render(request,'gestaoEscolar/gestor/diretor_form.html', context)
    else:
        dados = request.POST
        usuario_dados = {
            'email': dados['email'], 
            'username': dados['username'], 
            'password': dados['password'], 
            'password2': dados['password2']
        }
        gestor_dados = {
            'Nome': dados['Nome'], 
            'Sexo': dados['Sexo'], 
            'Data_Nascimento': dados['Data_Nascimento'], 
            'Cpf': dados['Cpf'], 
            'Rg': dados['Rg'], 
            'Usuario': '', 
            'Tipo_Gestor': 'D'
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
        telefone1_dados = {
            'Numero': dados['Numero1'], 
            'Pessoa': '', 
            'Escola': ''
        }
        telefone2_dados = {
            'Numero': dados['Numero2'], 
            'Pessoa': '', 
            'Escola': ''
        }
        gestor_form = GestorForm(gestor_dados)
        usuario_form = UsuarioForm(usuario_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone1_form = TelefoneForm(telefone1_dados)
        telefone2_form = TelefoneForm(telefone2_dados)
        erros_usuario = {}
        erros_gestor = {}
        erros_endereco = {}
        erros_telefone1 = {}
        erros_telefone2 = {}

        if not gestor_form.is_valid():
            erros_gestor = gestor_form.errors

        if not usuario_form.is_valid():
            erros_usuario = usuario_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone1_form.is_valid():
            erros_telefone1 = telefone1_form.errors

        if not telefone2_form.is_valid():
            erros_telefone2 = telefone2_form.errors

        if erros_usuario or erros_gestor or erros_endereco or erros_telefone1 or erros_telefone2:
            erros = []
            for erro in erros_gestor.values():
                erros.append(erro)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_usuario.values():
                erros.append(erro)
            for erro in erros_telefone1.values():
                erros.append(erro)
            for erro in erros_telefone2.values():
                erros.append(erro)
            context = {
                'Tipo_Sexo': TIPO_SEXO,
                'zonas': ZONAS,
                'erros':erros, 
                'gestor_dados':gestor_dados, 
                'usuario_dados': usuario_dados,
                'endereco_dados': endereco_dados,
                'telefone1_dados': telefone1_dados,   
                'telefone2_dados': telefone2_dados
            }
            return render(request,'gestaoEscolar/gestor/diretor_form.html', context)
        else:
            try:
                with transaction.atomic():
                    usuario = User.objects.create_user(
                        dados['username'], 
                        dados['email'], 
                        dados['password']
                    )
                    usuario.save()
                    endereco = endereco_form.save()
                    gestor_dados['Usuario'] = usuario.id
                    gestor_dados['Endereco'] = endereco.id
                    gestor_form = GestorForm(gestor_dados)
                    gestor = gestor_form.save()
                    telefone1_dados['Pessoa'] = gestor.id
                    telefone1_form = TelefoneForm(telefone1_dados)
                    telefone1_form.save()
                    telefone2_dados['Pessoa'] = gestor.id
                    telefone2_form = TelefoneForm(telefone2_dados)
                    telefone2_form.save()
                    return redirect('gestao_escolar_inicio')
            except Error:
                #Erros de servidor (500)
                Error = 'Erro no servidor: '+Error
                erros = [Error]
                context = {
                    'Tipo_Sexo': TIPO_SEXO,
                    'zonas': ZONAS,
                    'erros':erros, 
                    'gestor_dados':gestor_dados, 
                    'usuario_dados': usuario_dados,
                    'endereco_dados': endereco_dados,
                    'telefone1_dados': telefone1_dados,   
                    'telefone2_dados': telefone2_dados
                }
                return render(request,'gestaoEscolar/gestor/diretor_form.html', context)


@login_required
def escola_novo(request):
    NIVEIS = Escola.NIVEIS_DE_ESCOLARIDADE
    TIPOS = Escola.TIPOS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        context = {'Niveis': NIVEIS, 'Tipos': TIPOS, 'zonas': ZONAS}
        return render(request,'gestaoEscolar/escola/escola_form.html',context)
    else:
        dados = request.POST
        escola_dados = {
            'Nome': dados['Nome'], 
            'Email': dados['Email'], 
            'Nivel_Escolaridade': dados['Nivel_Escolaridade'], 
            'Tipo_Escola': dados['Tipo_Escola'], 
            'Nota_de_Corte': dados['Nota_de_Corte'], 
            'Diretor': '',
            'Endereco': ''
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
        telefone1_dados = {
            'Numero': dados['Numero1'], 
            'Pessoa': '', 
            'Escola': ''
        }
        telefone2_dados = {
            'Numero': dados['Numero2'], 
            'Pessoa': '', 
            'Escola': ''
        }
        telefone3_dados = {
            'Numero': dados['Numero3'], 
            'Pessoa': '', 
            'Escola': ''
        }
        escola_form = EscolaForm(escola_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone1_form = TelefoneForm(telefone1_dados)
        telefone2_form = TelefoneForm(telefone2_dados)
        telefone3_form = TelefoneForm(telefone3_dados)
        erros_escola = {}
        erros_endereco = {}
        erros_telefone1 = {}
        erros_telefone2 = {}
        erros_telefone3 = {}

        if not escola_form.is_valid():
            erros_escola = escola_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone1_form.is_valid():
            erros_telefone1 = telefone1_form.errors

        if not telefone2_form.is_valid():
            erros_telefone2 = telefone2_form.errors

        if not telefone3_form.is_valid():
            erros_telefone3 = telefone3_form.errors

        if erros_escola or erros_endereco or erros_telefone1 or erros_telefone2 or erros_telefone3:
            erros = []
            for erro in erros_escola.values():
                erros.append(erro)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone1.values():
                erros.append(erro)
            for erro in erros_telefone2.values():
                erros.append(erro)
            for erro in erros_telefone3.values():
                erros.append(erro)
            context = {
                'Niveis': NIVEIS, 
                'Tipos': TIPOS, 
                'zonas': ZONAS,
                'erros':erros, 
                'escola_dados': escola_dados,
                'endereco_dados': endereco_dados,       
                'telefone1_dados': telefone1_dados,   
                'telefone2_dados': telefone2_dados,     
                'telefone3_dados': telefone3_dados 
            }
            return render(request,'gestaoEscolar/escola/escola_form.html',context)
        else:
            try:
                with transaction.atomic():
                    endereco = endereco_form.save()
                    escola_dados['Endereco'] = endereco.id
                    diretor = obter_pessoa(request.user.username, 'Gestor')
                    escola_dados['Diretor'] = diretor.id
                    escola_form = EscolaForm(escola_dados)
                    escola = escola_form.save()
                    telefone1_dados['Escola'] = escola.id
                    telefone1_form = TelefoneForm(telefone1_dados)
                    telefone1_form.save()
                    telefone2_dados['Escola'] = escola.id
                    telefone2_form = TelefoneForm(telefone2_dados)
                    telefone2_form.save()
                    telefone3_dados['Escola'] = escola.id
                    telefone3_form = TelefoneForm(telefone3_dados)
                    telefone3_form.save()
                    diretor.tornar_diretor(escola,0) 
                    return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                Error = 'Erro no servidor: '+str(Error)
                erros = [Error]
                context = {
                    'Niveis': NIVEIS, 
                    'Tipos': TIPOS, 
                    'zonas': ZONAS,
                    'erros':erros, 
                    'escola_dados': escola_dados,
                    'endereco_dados': endereco_dados,       
                    'telefone1_dados': telefone1_dados,   
                    'telefone2_dados': telefone2_dados,     
                    'telefone3_dados': telefone3_dados 
                }
                return render(request,'gestaoEscolar/escola/escola_form.html',context)


@login_required
def escola_alterar(request,id):
    NIVEIS = Escola.NIVEIS_DE_ESCOLARIDADE
    TIPOS = Escola.TIPOS
    ZONAS = Endereco.TIPOS_ZONAS
    if request.method == 'GET':
        escola = Escola.objects.get(id=id)
        endereco = Endereco.objects.get(id=escola.Endereco)
        telefone1 = Telefone.objects.filter()
    #Testar a ordem em que os telefones aparecem 
    # (Talvez devesse colocar telefone nos objetos ao inves de ter os obj nos telefones)


        context = {
                'Niveis': NIVEIS, 
                'Tipos': TIPOS, 
                'zonas': ZONAS,
                'escola_dados': escola_dados,
                'endereco_dados': endereco_dados,       
                'telefone1_dados': telefone1_dados,   
                'telefone2_dados': telefone2_dados,     
                'telefone3_dados': telefone3_dados 
        }
        return render(request,'gestaoEscolar/escola/escola_form.html',context)
    else:
        dados = request.POST
        escola_dados = {
            'Nome': dados['Nome'], 
            'Email': dados['Email'], 
            'Nivel_Escolaridade': dados['Nivel_Escolaridade'], 
            'Tipo_Escola': dados['Tipo_Escola'], 
            'Nota_de_Corte': dados['Nota_de_Corte'], 
            'Diretor': '',
            'Endereco': ''
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
        telefone1_dados = {
            'Numero': dados['Numero1'], 
            'Pessoa': '', 
            'Escola': ''
        }
        telefone2_dados = {
            'Numero': dados['Numero2'], 
            'Pessoa': '', 
            'Escola': ''
        }
        telefone3_dados = {
            'Numero': dados['Numero3'], 
            'Pessoa': '', 
            'Escola': ''
        }
        escola_form = EscolaForm(escola_dados)
        endereco_form = EnderecoForm(endereco_dados)
        telefone1_form = TelefoneForm(telefone1_dados)
        telefone2_form = TelefoneForm(telefone2_dados)
        telefone3_form = TelefoneForm(telefone3_dados)
        erros_escola = {}
        erros_endereco = {}
        erros_telefone1 = {}
        erros_telefone2 = {}
        erros_telefone3 = {}

        if not escola_form.is_valid():
            erros_escola = escola_form.errors

        if not endereco_form.is_valid():
            erros_endereco = endereco_form.errors

        if not telefone1_form.is_valid():
            erros_telefone1 = telefone1_form.errors

        if not telefone2_form.is_valid():
            erros_telefone2 = telefone2_form.errors

        if not telefone3_form.is_valid():
            erros_telefone3 = telefone3_form.errors

        if erros_escola or erros_endereco or erros_telefone1 or erros_telefone2 or erros_telefone3:
            erros = []
            for erro in erros_escola.values():
                erros.append(erro)
            for erro in erros_endereco.values():
                erros.append(erro)
            for erro in erros_telefone1.values():
                erros.append(erro)
            for erro in erros_telefone2.values():
                erros.append(erro)
            for erro in erros_telefone3.values():
                erros.append(erro)
            context = {
                'Niveis': NIVEIS, 
                'Tipos': TIPOS, 
                'zonas': ZONAS,
                'erros':erros, 
                'escola_dados': escola_dados,
                'endereco_dados': endereco_dados,       
                'telefone1_dados': telefone1_dados,   
                'telefone2_dados': telefone2_dados,     
                'telefone3_dados': telefone3_dados 
            }
            return render(request,'gestaoEscolar/escola/escola_form.html',context)
        else:
            try:
                with transaction.atomic():
                    endereco = endereco_form.save()
                    escola_dados['Endereco'] = endereco.id
                    diretor = obter_pessoa(request.user.username, 'Gestor')
                    escola_dados['Diretor'] = diretor.id
                    escola_form = EscolaForm(escola_dados)
                    escola = escola_form.save()
                    telefone1_dados['Escola'] = escola.id
                    telefone1_form = TelefoneForm(telefone1_dados)
                    telefone1_form.save()
                    telefone2_dados['Escola'] = escola.id
                    telefone2_form = TelefoneForm(telefone2_dados)
                    telefone2_form.save()
                    telefone3_dados['Escola'] = escola.id
                    telefone3_form = TelefoneForm(telefone3_dados)
                    telefone3_form.save()
                    diretor.tornar_diretor(escola,0) 
                    return redirect('gestao_escolar_inicio')
            except Exception as Error:
                #Erros de servidor (500)
                Error = 'Erro no servidor: '+str(Error)
                erros = [Error]
                context = {
                    'Niveis': NIVEIS, 
                    'Tipos': TIPOS, 
                    'zonas': ZONAS,
                    'erros':erros, 
                    'escola_dados': escola_dados,
                    'endereco_dados': endereco_dados,       
                    'telefone1_dados': telefone1_dados,   
                    'telefone2_dados': telefone2_dados,     
                    'telefone3_dados': telefone3_dados 
                }
                return render(request,'gestaoEscolar/escola/escola_form.html',context)