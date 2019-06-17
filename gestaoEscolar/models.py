from django.db import models


class Escola(models.Model):
    Nome = models.CharField(max_length=50)
    Email = models.EmailField(max_length=254)
    FUNDAMENTAL = 'F'
    MEDIO = 'M'
    FUNDAMENTAL_MEDIO = 'FM'
    NIVEIS_DE_ESCOLARIDADE = (
        (FUNDAMENTAL,'Ensino Fundamental'),
        (MEDIO,'Ensino Médio'),
        (FUNDAMENTAL_MEDIO,'Ensino Fundamental e Médio')
    )
    Nivel_Escolaridade = models.CharField(
        max_length=20, 
        choices=NIVEIS_DE_ESCOLARIDADE,
        default=FUNDAMENTAL
    )
    PUBLICA = 'Pub'
    PRIVADA = 'Pri'
    TIPOS = (
        (PUBLICA,'Pública'),
        (PRIVADA,'Privada')
    )
    Tipo_Escola = models.CharField(max_length=20, choices=TIPOS, default=PUBLICA)
    #FKs
    Diretor = ''
    Endereco = ''


    def __str__(self):
        return self.Nome


class Telefone(models.Model):
    Numero = models.CharField(max_length=20)
    #FK
    Pessoa = '' #OPCIONAL CASO FOR DE UMA ESCOLA
    Escola = models.ForeignKey('Escola', on_delete=models.PROTECT)

    def __str__(self):
        return self.Numero


class Endereco(models.Model):
    Rua = models.CharField(max_length=40)
    Numero = models.PositiveSmallIntegerField()
    Bairro = models.CharField(max_length=40)
    Cidade = models.CharField(max_length=40)
    Estado = models.CharField(max_length=2)
    Complemento = models.CharField(max_length=100)
    URBANA = 'URB'
    RURAL = 'RUR'
    TIPOS_ZONAS = (
        (URBANA,'Urbana'),
        (RURAL,'Rural')
    )
    Zona = models.CharField(max_length=15, choices=TIPOS_ZONAS, default=URBANA)
    #FK
    Pessoa = 'OPCIONAL CASO FOR DE UMA ESCOLA'
    Escola = models.ForeignKey('Escola', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.Rua+' N°'+ str(self.Numero)


class Pessoa(models.Model):
    Nome = models.CharField(max_length=50)
    MASCULINO = 'M'
    FEMININO = 'F'
    TIPO_SEXO = (
        (MASCULINO,'Masculino'),
        (FEMININO,'Feminino')
    )
    Sexo = models.CharField(max_length=1, choices=TIPO_SEXO, default=MASCULINO)
    Data_Nascimento = models.DateField()
    Cpf = models.CharField(max_length=11,blank=True, null=True)
    Rg = models.CharField(max_length=9, blank=True, null=True)
    Nome_Usuario = 'models.CharField(max_length=40, unique=True)'
    Email = 'models.EmailField(max_length=254)'

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.Nome
    

class Gestor(Pessoa):
    pass


class Secretaria(Pessoa):
    pass


class Professor(Pessoa):
    ESPECIALISTA = 'E'
    MESTRE = 'M'
    DOUTOR = 'D'
    TIPOS_TITULOS = (
        (ESPECIALISTA, 'Especialista'),
        (MESTRE, 'Mestre'),
        (DOUTOR, 'Doutor')
    )
    Titulo = models.CharField(max_length=20, choices=TIPOS_TITULOS, default=ESPECIALISTA)



class Aluno(Pessoa):
    pass