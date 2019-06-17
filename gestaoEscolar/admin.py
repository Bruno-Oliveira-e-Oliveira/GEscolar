from django.contrib import admin
from .models import (
    Escola,
    Telefone,
    Endereco,
    Gestor,
    Secretaria,
    Professor,
    Aluno
)

# Register your models here.

admin.site.register(Escola)
admin.site.register(Telefone)
admin.site.register(Endereco)
admin.site.register(Gestor)
admin.site.register(Secretaria)
admin.site.register(Professor)
admin.site.register(Aluno)

