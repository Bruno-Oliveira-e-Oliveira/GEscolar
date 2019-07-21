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
    Turma,
    Aula,
    Avaliacao,
    Frequencia,
    Aplicacao,
    Matricula,
    AnoLetivo,
    Bimestre,
    Nota,
    Matricula_Turma
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
admin.site.register(Aula)
admin.site.register(Avaliacao)
admin.site.register(Frequencia)
admin.site.register(Aplicacao)
admin.site.register(Matricula)
admin.site.register(AnoLetivo)
admin.site.register(Bimestre)
admin.site.register(Nota)
admin.site.register(Matricula_Turma)



