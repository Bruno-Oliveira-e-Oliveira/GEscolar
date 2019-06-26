from django.forms import ModelForm
from django import forms
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

class GestorForm(ModelForm):
    class Meta:
        model = Gestor
        fields = '__all__'


class UsuarioForm(ModelForm):
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email','password', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError(
                'As senhas apresentam diferenças.'
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