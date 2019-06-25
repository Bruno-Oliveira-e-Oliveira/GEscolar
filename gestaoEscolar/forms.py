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
from django.contrib.auth.models import User

class UsuarioLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


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