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
    Diretor = models.OneToOneField('Gestor', on_delete=models.PROTECT,blank=True, null=True)
    Endereco = models.OneToOneField('Endereco', on_delete=models.PROTECT)

    def __str__(self):
        return self.Nome


class Telefone(models.Model):
    Numero = models.CharField(max_length=20)
    #FK
    Pessoa = models.ForeignKey('Pessoa', on_delete=models.PROTECT, blank=True, null=True)
    Escola = models.ForeignKey('Escola', on_delete=models.PROTECT, blank=True, null=True)

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
    #Controlar para quem é obrigatório 
    Pessoa = models.ForeignKey('Pessoa', on_delete=models.PROTECT, blank=True, null=True)
    
    def __str__(self):
        return self.Rua+' N°'+ str(self.Numero)


class PessoaAbstract(models.Model):
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
    #Controlar para quem é obrigatório 
    Escola = models.ForeignKey('Escola', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.Nome


class Pessoa(PessoaAbstract):
    pass
    

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
    Ra = models.CharField(max_length=20,blank=True, null=True, unique=True)
    Cidade_Nascimento = models.CharField(max_length=40)
    Estado_Nascimento = models.CharField(max_length=40)
    Nacionalidade = models.CharField(max_length=20)
    SIM = 'S'
    NAO = 'N'
    SIM_NAO = (
        (SIM, 'Sim'),
        (NAO, 'Não')
    )
    Irmao_Gemeo = models.CharField(max_length=10, choices=SIM_NAO, default=SIM)
    Nome_Pai = models.CharField(max_length=40)
    Nome_Mae = models.CharField(max_length=40)
    Necessidade_Educacional_Especial = models.CharField(max_length=10, choices=SIM_NAO, default=SIM)
    Superdotacao = models.CharField(max_length=10, choices=SIM_NAO, default=SIM)
    MULTIPLA = 'multipla'
    CEGUEIRA = 'cegueira'
    BAIXA_VISAO = 'baixa_visao'
    SURDEZ_SEVERA_OU_PROFUNDA = 'surdez_severa_ou_profunda'  
    SURDEZ_SEVERA_OU_MODERADA = 'surdez_severa_ou_moderada' 
    SURDOCEGUEIRA = 'surdocegueira'
    FISICA_PARALISIA_CEREBRAL = 'fisica_paralisia_cerebral'
    FISICA_CADEIRANTE = 'fisica_cadeirante'
    FISICA_OUTROS = 'fisica_outros'
    SINDROME_DE_DOWN = 'sindrome_de_down'
    INTELECTUAL = 'intelectual'
    NAO_POSSUI = 'nao_possui'
    TIPOS_DEFICIENCIA = (
        (NAO_POSSUI, 'Não Possui'),
        (MULTIPLA, 'Múltipla'),
        (CEGUEIRA, 'Cegueira'),
        (BAIXA_VISAO, 'Baixa Visão'),
        (SURDEZ_SEVERA_OU_PROFUNDA, 'Surdez Severa ou Profunda'),
        (SURDEZ_SEVERA_OU_MODERADA, 'Surdez Leve ou Moderada'),
        (SURDOCEGUEIRA, 'Surdocegueira'),
        (FISICA_PARALISIA_CEREBRAL, 'Física – Paralisia Cerebral'),
        (FISICA_CADEIRANTE, 'Física – Cadeirante'),
        (FISICA_OUTROS, 'Física – Outros'),
        (SINDROME_DE_DOWN, 'Síndrome de Down'),
        (INTELECTUAL, 'Intelectual')
    )
    Deficiencia = models.CharField(max_length=40, choices=TIPOS_DEFICIENCIA, default=NAO_POSSUI)
    AUTISTA_INFANTIL = 'autista_infantil'
    SINDROME_DE_ASPERGER = 'sindrome_de_asperger'
    SINDROME_DE_RETT = 'sindrome_de_rett'
    TRANSTORNO_DESINTEGRATIVO_DE_INFANCIA = 'transtorno_desintegrativo_de_infancia'
    TIPOS_TRANSTORNO = (
        (NAO_POSSUI, 'Não Possui'),
        (AUTISTA_INFANTIL, 'Autista Infantil'),
        (SINDROME_DE_ASPERGER, 'Síndrome de Asperger'),
        (SINDROME_DE_RETT, 'Síndrome de Rett'),
        (TRANSTORNO_DESINTEGRATIVO_DE_INFANCIA, 'Transtorno Desintegrativo de Infância')
    )
    Transtorno_Global_do_Desenvolvimento = models.CharField(
        max_length=40, 
        choices=TIPOS_TRANSTORNO, 
        default=NAO_POSSUI
    )
    Bolsa_Familia = models.CharField(max_length=10, choices=SIM_NAO, default=SIM)
    
    
    
    
    
     
    
    
    

    