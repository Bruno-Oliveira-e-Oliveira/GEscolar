from django.contrib.auth.decorators import PermissionDenied

def checarPermEscola(objeto, escola):
    if objeto.Escola == escola:
        raise PermissionDenied
