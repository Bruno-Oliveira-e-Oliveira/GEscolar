from django.contrib.auth.decorators import PermissionDenied
from django.contrib.auth.models import Group

def checarPermEscola(objeto, escola):
    if objeto.Escola.id != escola.id:
        raise PermissionDenied


def checarEscola(escola_id_sessao, escola_id_parametro):
    if escola_id_sessao != escola_id_parametro:
        raise PermissionDenied   


def checarGestor(gestor_id_sessao, gestor_id_parametro):  
    if gestor_id_sessao != gestor_id_parametro:
        raise PermissionDenied   


def checarPermObj(perm, user):
    if not user.has_perm(perm,obj=None):
        raise PermissionDenied


def configurar_grupos(tipo,usuario):
	if tipo == 'G':
		nome = 'Diretor'
	elif tipo == 'S':
		nome = 'Secretario'
	elif tipo == 'P':
		nome = 'Professor'
	elif tipo == 'A':
		nome = 'Aluno'
	grupo = Group.objects.get(name=nome)
	usuario.groups.add(grupo)


def limpar_grupos(usuario):
	usuario.groups.clear()