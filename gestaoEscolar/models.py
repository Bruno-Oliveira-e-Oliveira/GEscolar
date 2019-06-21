from django.db import models


class Escola(models.Model):
    Nome = models.CharField('Nome',max_length=50)
    Email = models.EmailField('Email',max_length=254)
    FUNDAMENTAL = 'F'
    MEDIO = 'M'
    FUNDAMENTAL_MEDIO = 'FM'
    NIVEIS_DE_ESCOLARIDADE = (
        (FUNDAMENTAL,'Ensino Fundamental'),
        (MEDIO,'Ensino Médio'),
        (FUNDAMENTAL_MEDIO,'Ensino Fundamental e Médio')
    )
    Nivel_Escolaridade = models.CharField(
        'Nível Escolaridade',
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
    Tipo_Escola = models.CharField('Tipo da Escola',max_length=20, choices=TIPOS, default=PUBLICA)
    #NOVO CAMPO
    Nota_de_Corte = models.PositiveSmallIntegerField(verbose_name = 'Nota de corte de aprovação')
    Diretor = models.OneToOneField(
        'Gestor', 
        on_delete = models.PROTECT,
        blank = True, 
        null = True,
        verbose_name = 'Diretor'
    )
    Endereco = models.OneToOneField('Endereco', on_delete=models.PROTECT,verbose_name = 'Endereço')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Email'], name='unique_email_escola'),
            models.UniqueConstraint(fields=['Nome','Endereco'], name='unique_endereco_escola')
        ]
    
    def __str__(self):
        return self.Nome


class Telefone(models.Model):
    Numero = models.CharField('Número',max_length=20)
    #FK
    Pessoa = models.ForeignKey(
        'Pessoa',
        on_delete = models.PROTECT,
        blank = True, 
        null=True,
        verbose_name = 'Pessoa'
    )
    Escola = models.ForeignKey(
        'Escola', 
        on_delete = models.PROTECT, 
        blank = True, 
        null = True,
        verbose_name = 'Escola'
    )

    def __str__(self):
        return self.Numero


class Endereco(models.Model):
    Rua = models.CharField('Rua',max_length=40)
    Numero = models.PositiveSmallIntegerField(verbose_name = 'Número')
    Bairro = models.CharField('Bairro',max_length=40)
    Cidade = models.CharField('Cidade',max_length=40)
    Estado = models.CharField('Estado',max_length=2)
    Complemento = models.CharField('Complemento',max_length=100)
    URBANA = 'URB'
    RURAL = 'RUR'
    TIPOS_ZONAS = (
        (URBANA,'Urbana'),
        (RURAL,'Rural')
    )
    Zona = models.CharField('Zona',max_length=15, choices=TIPOS_ZONAS, default=URBANA)
    #Controlar para quem é obrigatório 
    Pessoa = models.ForeignKey(
        'Pessoa',
        on_delete = models.PROTECT,
        blank = True, 
        null=True,
        verbose_name = 'Pessoa'
    )
    
    def __str__(self):
        return self.Rua+' N°'+ str(self.Numero)


class PessoaAbstract(models.Model):
    Nome = models.CharField('Nome',max_length=50)
    MASCULINO = 'M'
    FEMININO = 'F'
    TIPO_SEXO = (
        (MASCULINO,'Masculino'),
        (FEMININO,'Feminino')
    )
    Sexo = models.CharField('Sexo',max_length=1, choices=TIPO_SEXO, default=MASCULINO)
    Data_Nascimento = models.DateField(verbose_name = 'Data de Nascimento')
    Cpf = models.CharField('CPF',max_length=11,blank=True, null=True, unique=True)
    Rg = models.CharField('RG',max_length=9, blank=True, null=True, unique=True)
    Nome_Usuario = 'models.CharField(max_length=40, unique=True)'
    Email = 'models.EmailField(max_length=254)'
    #Controlar para quem é obrigatório 
    Escola = models.ForeignKey(
        'Escola', 
        on_delete = models.PROTECT, 
        blank = True, 
        null = True,
        verbose_name = 'Escola'
    )

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
    Titulo = models.CharField('Título',max_length=20, choices=TIPOS_TITULOS, default=ESPECIALISTA)


class Aluno(Pessoa):
    Ra = models.CharField('RA',max_length=20,blank=True, null=True, unique=True)
    Cidade_Nascimento = models.CharField('Cidade de Nascimento',max_length=40)
    Estado_Nascimento = models.CharField('Estado de Nascimento',max_length=40)
    Nacionalidade = models.CharField('Nacionalidade',max_length=20)
    SIM = 'S'
    NAO = 'N'
    SIM_NAO = (
        (SIM, 'Sim'),
        (NAO, 'Não')
    )
    Irmao_Gemeo = models.CharField('Irmão Gêmeo',max_length=10, choices=SIM_NAO, default=SIM)
    Nome_Pai = models.CharField('Nome do Pai',max_length=40)
    Nome_Mae = models.CharField('Nome da Mãe',max_length=40)
    Necessidade_Educacional_Especial = models.CharField(
        'Necessidade Educacional Especial',
        max_length = 10,
        choices = SIM_NAO, 
        default = SIM
    )
    Superdotacao = models.CharField(
        'Superdotação/Altas Habilidades',
        max_length = 10, 
        choices = SIM_NAO, 
        default = SIM
    )
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
    Deficiencia = models.CharField(
        'Deficiência',
        max_length = 40, 
        choices = TIPOS_DEFICIENCIA, 
        default = NAO_POSSUI
    )
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
        'Transtorno Global do Desenvolvimento',
        max_length=40, 
        choices=TIPOS_TRANSTORNO, 
        default=NAO_POSSUI
    )
    Bolsa_Familia = models.CharField(max_length=10, choices=SIM_NAO, default=SIM)
    Turma = models.ForeignKey(
        'Turma', 
        on_delete=models.PROTECT, 
        verbose_name='Turma'
    )

    def __str__(self):
        return self.Nome


class Matricula(models.Model):
    Rm = models.AutoField(primary_key=True, verbose_name='RM')
    Data = models.DateField(verbose_name = 'Data da realização da matrícula',auto_now=True)
    MATRICULADO = 'matriculado'
    CONCLUIDO = 'concluido'
    TRANSFERIDO = 'transferido'
    TRANCADO = 'trancado'
    TIPOS_SITUACAO = (
        (MATRICULADO, 'Matriculado'),
        (CONCLUIDO, 'Concluído'),
        (TRANSFERIDO, 'Transferido'),
        (TRANCADO, 'Trancado')
    )
    Situacao = models.CharField('Situação', max_length=20, choices=TIPOS_SITUACAO, default=MATRICULADO)
    Aluno = models.OneToOneField('Aluno', on_delete=models.PROTECT, verbose_name='Aluno')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    def __str__(self):
        return str(self.Rm) + ' - ' + self.Aluno.Nome + ' - ' + self.Situacao


#Tirar a funcionalidade de log de transferência?
# class Transferencia(models.Model):
#     SALA = 'sala'


class Disciplina(models.Model):
    Nome = models.CharField('Nome',max_length=20)
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Nome', 'Escola'], name='unique_Disciplina')
        ]
    
    def __str__(self):
        return self.Nome


class Leciona(models.Model):
    Aulas_Previstas = models.PositiveSmallIntegerField(verbose_name='Aulas Previstas')
    Disciplina = models.ForeignKey('Disciplina',on_delete=models.PROTECT, verbose_name='Disciplina')
    Turma = models.ForeignKey('Turma',on_delete=models.PROTECT, verbose_name='Turma')
    Professor = models.ForeignKey(
        'Professor',
        on_delete=models.PROTECT, 
        verbose_name='Professor',
        blank=True, 
        null=True
    )
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Disciplina', 'Turma', 'Escola'], name='unique_Leciona')
        ]

    def __str__(self):
        try:
            return self.Turma.Nome + ' - '+ self.Disciplina.Nome + ' - ' + self.Professor.Nome
        except:
            return self.Turma.Nome + ' - ' + self.Disciplina.Nome
            
         
class Turma(models.Model):
    Nome = models.CharField('Nome',max_length=20)
    MANHA = 'M'
    TARDE = 'T'
    TIPO_PERIODO = (
        (MANHA, 'Manhã'),
        (TARDE, 'Tarde')
    )
    Periodo = models.CharField(
        'Período',
        max_length = 20, 
        choices = TIPO_PERIODO, 
        default = MANHA
    )
    Nivel_Escolaridade = models.CharField('Nível Escolaridade',max_length=20)
    Sala = models.PositiveSmallIntegerField(verbose_name = 'Sala')
    Max_Alunos = models.PositiveSmallIntegerField(verbose_name = 'Máximo de Alunos')
    AnoLetivo = ''
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Nome', 'Escola'], name='unique_Turma'),
            models.UniqueConstraint(
                fields=['Sala','Periodo','Escola'], 
                name='unique_Sala_Turma_Periodo'
            )
        ]

    def __str__(self):
        return self.Nome

    def checarMaxAlunos(self):
        alunos = len(Aluno.objects.filter(Turma=self.id))

        if alunos < self.Max_Alunos:
            return True
        else:
            return False

    def matricularNaTurma(self,idAluno):
        pass


class Aula(models.Model):
    Data = models.DateField(verbose_name='Data')
    Turma = models.ForeignKey('Turma', on_delete=models.PROTECT, verbose_name='Turma')
    Leciona = models.ForeignKey('Leciona', on_delete=models.PROTECT, verbose_name='Leciona')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    def __str__(self):
        return self.Turma.Nome + ' - ' + self.Leciona.Disciplina.Nome + ' - ' + str(self.Data)

    def checarData(self):
        pass


class Avaliacao(models.Model):
    Tema = models.CharField('Tema', max_length=30)
    #Tirado o campo Nota máxima
    Peso = models.PositiveSmallIntegerField(verbose_name='Peso')
    Aula = models.ForeignKey('Aula', on_delete = models.PROTECT, verbose_name = 'Aula')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    def __str__(self):
        return self.Aula.Turma.Nome + ' - '+ self.Tema + ' - ' + str(self.Aula.Data)


class Frequencia(models.Model):
    #Campo Frequencia adicionado
    Presenca = models.BooleanField(verbose_name='Presença', default=True)
    Aula = models.ForeignKey('Aula', on_delete = models.PROTECT, verbose_name = 'Aula')
    Aluno = models.ForeignKey('Aluno', on_delete = models.PROTECT, verbose_name = 'Aluno')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Aula','Aluno'], 
                name='unique_Aula_Aluno'
            )
        ]
    
    def __str__(self):
        return self.Aula.Turma.Nome + ' - '+ self.Aluno.Nome + ' - ' + str(self.Aula.Data)


class Aplicacao(models.Model):
    Nota = models.DecimalField(verbose_name='Nota', max_digits=4, decimal_places=2)
    Avaliacao = models.ForeignKey('Avaliacao', on_delete = models.PROTECT, verbose_name = 'Avaliação')
    Aluno = models.ForeignKey('Aluno', on_delete = models.PROTECT, verbose_name = 'Aluno')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Avaliacao','Aluno'], 
                name='unique_Avaliacao_Aluno'
            )
        ]

    def __str__(self):
        return self.Avaliacao.Tema + ' - ' + str(self.Avaliacao.Aula.Data)

    
class AnoLetivo(models.Model):
    Ano = models.PositiveSmallIntegerField(verbose_name='Ano')
    Data_Inicio = models.DateField(verbose_name='Abertura do ano letivo')
    Data_Fim = models.DateField(verbose_name='Fechamento do ano letivo')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Ano','Escola'], 
                name='unique_Ano'
            )
        ]

    def __str__(self):
        return str(self.Ano)


class Bimestre(models.Model):
    AnoLetivo = models.ForeignKey('AnoLetivo', on_delete=models.PROTECT, verbose_name='Ano')
    Bimestre = models.PositiveSmallIntegerField(verbose_name='Bimestre')
    Data_Inicio = models.DateField(verbose_name='Abertura do bimestre')
    Data_Limite_Notas = models.DateField(verbose_name='Limite do lançamento das Notas')
    Data_Fim = models.DateField(verbose_name='Fechamento do bimestre')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['AnoLetivo','Bimestre','Escola'], 
                name='unique_Ano_Bimestre'
            )
        ]

    def __str__(self):
        return str(self.AnoLetivo) + ' - ' + str(self.Bimestre)


class Nota(models.Model):
    BIMESTRAL = 'B'
    FINAL = 'F'
    TIPOS_NOTA = (
        (BIMESTRAL, 'Bimestral'),
        (FINAL, 'Final')
    ) 
    Tipo = models.CharField('Tipo', max_length=20, choices=TIPOS_NOTA, default=BIMESTRAL)
    Valor = models.DecimalField(verbose_name='Nota', max_digits=4, decimal_places=2)
    Aluno = models.ForeignKey('Aluno', on_delete = models.PROTECT, verbose_name = 'Aluno')
    Leciona = models.ForeignKey('Leciona', on_delete=models.PROTECT, verbose_name='Leciona')
    AnoLetivo = models.ForeignKey('AnoLetivo',on_delete=models.PROTECT,verbose_name='Ano')
    Bimestre = models.ForeignKey(
        'Bimestre', 
        on_delete = models.PROTECT,
        verbose_name = 'Bimestre',
        blank = True, 
        null = True
    )
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=['AnoLetivo','Bimestre','Aluno','Leciona','Escola'], 
            name='unique_Ano_Bimestre_Aluno_Leciona'
        ),
        models.UniqueConstraint(
            fields=['AnoLetivo','Aluno','Leciona','Escola'], 
            name='unique_Ano_Aluno_Leciona'
        )
    ]

    def __str__(self):
        return self.Leciona.Disciplina.Nome + ' - ' + self.Tipo + ' - ' + self.Aluno.Nome
        

