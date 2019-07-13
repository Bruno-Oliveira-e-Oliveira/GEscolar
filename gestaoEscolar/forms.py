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


class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'

    def clean_Numero(self):
        numero_dados = self.cleaned_data['Numero']

        if numero_dados <= 0:
            raise forms.ValidationError(
                'Valor inválido para o campo Número.'
            )       
        return numero_dados 


class TelefoneForm(ModelForm):
    class Meta:
        model = Telefone
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


class UsuarioEmailForm(ModelForm):

    class Meta:
        model = User
        fields = ('email','is_active')


class EscolaForm(ModelForm):
    class Meta:
        model = Escola
        fields = '__all__'

    def clean_Nota_de_Corte(self):
        nota_dados = self.cleaned_data['Nota_de_Corte']

        if nota_dados > 10 or nota_dados <= 0:
            raise forms.ValidationError(
                'Valor inválido para o campo Nota.'
            )       
        return nota_dados     


class SecretarioForm(ModelForm):
    class Meta:
        model = Secretaria
        fields = '__all__'


class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = '__all__'


class MatriculaForm(ModelForm):
    class Meta:
        model = Matricula
        fields = ('Situacao',)
    

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