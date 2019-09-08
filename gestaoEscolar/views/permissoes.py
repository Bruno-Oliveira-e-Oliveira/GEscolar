from django.contrib.auth.decorators import PermissionDenied

def checarPermEscola(objeto, escola):
    if objeto.Escola.id != escola.id:
        raise PermissionDenied

def checarEscola(escola_id_sessao, escola_id_parametro):
    if escola_id_sessao != escola_id_parametro:
        raise PermissionDenied        

def checarPermObj(perm, user):
    if not user.has_perm(perm,obj=None):
        raise PermissionDenied