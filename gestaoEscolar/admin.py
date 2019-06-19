from django.contrib import admin
from .models import (
    Escola,
    Telefone,
    Endereco,
    Gestor,
    Secretaria,
    Professor,
    Aluno,
    Disciplina,
    Leciona,
    Turma
)

# Register your models here.

admin.site.register(Escola)
admin.site.register(Telefone)
admin.site.register(Endereco)
admin.site.register(Gestor)
admin.site.register(Secretaria)
admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Disciplina)
admin.site.register(Leciona)
admin.site.register(Turma)

