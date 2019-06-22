from django.forms import ModelForm
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
    Nota
)


class EscolaForm(ModelForm):
    class Meta:
        model = Escola
        fields = '__all__'


    

    # Telefone

    # Endereco

    # Gestor

    # Secretaria

    # Professor

    # Aluno

    # Disciplina

    # Leciona

    # Turma

    # Aula

    # Avaliacao

    # Frequencia

    # Aplicacao

    # Matricula

    # AnoLetivo

    # Bimestre

    # Nota