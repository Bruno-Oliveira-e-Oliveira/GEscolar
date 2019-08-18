from django.db import models
from django.contrib.auth.models import User


class Escola(models.Model):
    Nome = models.CharField('Nome',max_length=50)
    Email = models.EmailField('Email',max_length=254,unique=True)
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
    Nota_de_Corte = models.IntegerField(
        verbose_name = 'Nota de corte de aprovação',
        error_messages = {
            'max_value': 
            'Certifique-se que o valor do campo "Número" seja menor ou igual a 4294967295.'
        }
    )
    Diretor = models.OneToOneField(
        'Gestor', 
        on_delete = models.PROTECT,
        blank = True, 
        null = True,
        verbose_name = 'Diretor'
    )
    Endereco = models.OneToOneField(
        'Endereco', 
        on_delete = models.PROTECT,
        verbose_name = 'Endereço',
        blank=True, 
        null=True
    )
    Telefone = models.OneToOneField(
        'Telefone', 
        on_delete = models.PROTECT,
        verbose_name = 'Telefone',
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return self.Nome

    def retornar_nivel(self):
        if self.Nivel_Escolaridade == 'F':
            return (('F','Ensino Fundamental'),)
        elif self.Nivel_Escolaridade == 'M':
            return (('M','Ensino Médio'),)
        elif self.Nivel_Escolaridade == 'FM':
            return (('F','Ensino Fundamental'),('M','Ensino Médio'))

class Telefone(models.Model):
    Numero1 = models.CharField('Número 1',max_length=20)
    Numero2 = models.CharField('Número 2',max_length=20)

    def __str__(self):
        return self.Numero1 


class Endereco(models.Model):
    Rua = models.CharField('Rua',max_length=40)
    Numero = models.IntegerField(
        verbose_name = 'Número', 
        error_messages = {
            'max_value': 
            'Certifique-se que o valor do campo "Número" seja menor ou igual a 4294967295.'
        }
    )
    Bairro = models.CharField('Bairro',max_length=40)
    Cidade = models.CharField('Cidade',max_length=40)
    Estado = models.CharField('Estado',max_length=2)
    Complemento = models.CharField('Complemento',max_length=100, blank=True, null=True)
    URBANA = 'URB'
    RURAL = 'RUR'
    TIPOS_ZONAS = (
        (URBANA,'Urbana'),
        (RURAL,'Rural')
    )
    Zona = models.CharField('Zona',max_length=15, choices=TIPOS_ZONAS, default=URBANA)
    
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
    Usuario = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    #Adicionar o campo Tipo Pessoa
    GESTOR = 'G'
    DIRETOR = 'D'
    SECRETARIO = 'S'
    PROFESSOR = 'P'
    ALUNO = 'A'
    TIPO_CONTA = (
        (GESTOR, 'Gestor'),
        (DIRETOR, 'Diretor'),
        (SECRETARIO, 'Secretário'),
        (PROFESSOR, 'Professor'),
        (ALUNO, 'Aluno')
    )
    Tipo_Pessoa = models.CharField('Tipo de Pessoa', max_length=20, choices=TIPO_CONTA)
    ATIVO = True
    INATIVO = False
    STATUS = (
        (ATIVO, 'Ativo'),
        (INATIVO, 'Inativo')
    )
    Endereco = models.OneToOneField(
        'Endereco', 
        on_delete = models.PROTECT,
        verbose_name = 'Endereço',
        blank=True, 
        null=True
    )
    Telefone = models.OneToOneField(
        'Telefone', 
        on_delete = models.PROTECT,
        verbose_name = 'Telefone',
        blank=True, 
        null=True
    )
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
    
    def obter_pessoa(nome_usuario, tipo):
        if nome_usuario:
            usuario = User.objects.get(username=nome_usuario)
            if tipo == 'Gestor':
                pessoa = Gestor.objects.filter(Usuario=usuario.id)
            elif tipo == 'Secretaria':
                pessoa = Secretaria.objects.filter(Usuario=usuario.id)
            elif tipo == 'Professor':
                pessoa = Professor.objects.filter(Usuario=usuario.id)
            elif tipo == 'Aluno':
                pessoa = Aluno.objects.filter(Usuario=usuario.id)
            else:
                pessoa = Pessoa.objects.filter(Usuario=usuario.id)
            
            return pessoa[0]
        else:
            return None



class Pessoa(PessoaAbstract):
    pass
    

class Gestor(Pessoa):
    def tornar_diretor(self, escola, diretor_anterior):
        # if diretor_anterior:
        #     achou = Gestor.objects.filter(id=diretor_anterior.id, Escola=escola.id).exists()
        #     if achou:
        #         diretor_anterior.tirar_cargo_diretor()
        #         self.Escola = escola
        #         return True
        #     else:
        #         return False
        # else:
        #     achou = Gestor.objects.filter(Escola=escola.id).exists()
        #     if not achou:
        #         self.Escola = escola
        #         return True
        #     else:
        #         return False
        self.Escola = escola
        self.save() 

    def tirar_cargo_diretor(self):
        self.Escola = None
            

#Mudar para secretario
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

    def __str__(self):
        return self.Nome

    def retornar_alunos_sem_turma(escolaid):
        alunos = Aluno.objects.filter(Escola=escolaid)
        if len(alunos) == 0:
            return 0
        else:
            ano = AnoLetivo.retornar_ativo(escolaid)  
            alunos_sem_turma = []
            if ano is not None:
                turmas_ativas = Turma.objects.filter(Escola=escolaid, AnoLetivo=ano.id) 
                if len(turmas_ativas) == 0:
                    return alunos
                else:
                    for aluno in alunos:
                        achou = False
                        for turma in turmas_ativas:
                            matriculas = Matricula_Turma.objects.filter(Escola=escolaid, Turma=turma.id)
                            for matricula in matriculas:
                                if matricula.Aluno.id == aluno.id:
                                    achou = True
                        if not achou:
                            alunos_sem_turma.append(aluno)
                    if len(alunos_sem_turma) == 0:
                        return -2
                    else:
                        return alunos_sem_turma
            else:
                return -1


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
    Aulas_Previstas = models.PositiveSmallIntegerField(verbose_name='Aulas Previstas', blank=True, null=True)
    Matriz_Item = models.ForeignKey('Matriz_Item',on_delete=models.PROTECT, verbose_name='Matriz_Item')
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
            models.UniqueConstraint(fields=['Matriz_Item', 'Turma', 'Escola'], name='unique_Leciona_Matriz_Item')
        ]

    def __str__(self):
        return self.Turma.Nome + ' - ' + self.Matriz_Item.Disciplina.Nome

    def gerar_lecionas(turma):
        itens = Matriz_Item.objects.filter(Serie=turma.Serie.id)
        for item in itens:
            leciona = Leciona(Matriz_Item=item, Turma=turma, Escola=turma.Escola)
            leciona.save()
    
    def atualizar_lecionas_turma(tipo_transacao, item, escolaid):
        achou = Turma.objects.filter(Escola=escolaid).exists()
        escola = Escola.objects.get(id=escolaid)
        if achou:
            turmas = Turma.objects.filter(Escola=escolaid, Serie=item.Serie.id)
            if tipo_transacao == 'INS':
                for turma in turmas:
                    leciona = Leciona(Matriz_Item=item, Turma=turma, Escola=escola)
                    leciona.save()
            elif tipo_transacao == 'DEL':
                for turma in turmas:
                    lecionas = Leciona.objects.filter(Matriz_Item=item.id, Turma=turma.id)
                    if len(lecionas) > 0:
                        lecionas[0].delete()

    @property
    def nome_editado(self):
        if self.Professor is not None:
            return self.Matriz_Item.Disciplina.Nome + ' - ' + self.Professor.Nome
        else:
            return self.Matriz_Item.Disciplina.Nome + ' - Não há professor associado à essa disciplina.'        


class Turma(models.Model):
    Nome = models.CharField('Nome',max_length=1)
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
    Sala = models.PositiveSmallIntegerField(verbose_name = 'Sala')
    Max_Alunos = models.PositiveSmallIntegerField(verbose_name = 'Máximo de Alunos')
    Serie = models.ForeignKey('Serie', on_delete = models.PROTECT, verbose_name = 'Serie')
    AnoLetivo = models.ForeignKey(
        'AnoLetivo', 
        on_delete = models.PROTECT, 
        verbose_name = 'Ano',
        blank=True, 
        null=True
    )
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Nome', 'Serie', 'AnoLetivo', 'Escola'], 
                name='unique_Turma_Serie_Ano'
            ),
            models.UniqueConstraint(
                fields=['Sala', 'Periodo', 'AnoLetivo', 'Escola'], 
                name='unique_Sala_Turma_Periodo'
            )
        ]

    @property
    def nome_editado(self):
        if self.Serie.Nivel_Escolaridade == 'F':
            return str(self.Serie.Numero) +''+ self.Nome +' - Ensino Fundamental'
        else:
            return str(self.Serie.Numero) +''+ self.Nome +' - Ensino Médio'

    def __str__(self):
        if self.Serie.Nivel_Escolaridade == 'F':
            return str(self.Serie.Numero) +''+ self.Nome +' - Ensino Fundamental'
        else:
            return str(self.Serie.Numero) +''+ self.Nome +' - Ensino Médio'

    def checarMaxAlunos(self):
        matriculas = Matricula_Turma.objects.filter(Turma=self.id)

        if len(matriculas) < self.Max_Alunos:
            return True
        else:
            return False

    
class Matricula_Turma(models.Model):
    Turma = models.ForeignKey('Turma', on_delete=models.PROTECT, verbose_name='Turma')
    Aluno = models.ForeignKey('Aluno', on_delete = models.PROTECT, verbose_name = 'Aluno')
    MATRICULADO = 'matriculado'
    CONCLUIDO = 'concluido'
    TRANSFERIDO = 'transferido'
    TRANCADO = 'trancado'
    REPROVADO = 'reprovado'
    TIPOS_SITUACAO = (
        (MATRICULADO, 'Matriculado'),
        (CONCLUIDO, 'Concluído'),
        (TRANSFERIDO, 'Transferido'),
        (TRANCADO, 'Trancado'),
        (REPROVADO, 'Reprovado')
    )
    Situacao = models.CharField('Situação', max_length=20, choices=TIPOS_SITUACAO, default=MATRICULADO)
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    def __str__(self):
        return self.Turma.Nome + ' - ' + self.Aluno.Nome

    def retornar_alunos_matriculados(turma, escola):
        matriculas = Matricula_Turma.objects.filter(Escola=escola.id, Turma=turma.id)
        alunos = []
        if len(matriculas) > 0:
            for matricula in matriculas:
                alunos.append(matricula.Aluno)
        return alunos


class Aula(models.Model):
    Data = models.DateField(verbose_name='Data')
    Tema = models.CharField('Tema',max_length=40)
    Turma = models.ForeignKey('Turma', on_delete=models.PROTECT, verbose_name='Turma')
    Leciona = models.ForeignKey('Leciona', on_delete=models.PROTECT, verbose_name='Leciona')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')

    def __str__(self):
        return self.Turma.Nome + ' - ' + self.Leciona.Matriz_Item.Disciplina.Nome + ' - ' + str(self.Data)


class Frequencia(models.Model):
    PRESENTE = 'Presente'
    AUSENTE = 'Ausente'
    SITUACAO = (
        (PRESENTE, 'Presente'),
        (AUSENTE, 'Ausente')
    )
    Presenca = models.CharField('Tema',max_length=10, choices=SITUACAO, default=PRESENTE)
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

    def gerar_frequencias(aula, escola):
        alunos = Matricula_Turma.retornar_alunos_matriculados(aula.Turma, escola)
        for aluno in alunos:
            frequencia = Frequencia(Aula=aula, Aluno=aluno, Escola=escola)
            frequencia.save()

    def apagar_frequencias(aula, escola):
        frequencias = Frequencia.objects.filter(Escola=escola.id, Aula=aula.id)
        for frequencia in frequencias:
            frequencia.delete()

    def apagar_frequencias_aluno(aluno, escola):
        frequencias = Frequencia.objects.filter(Escola=escola.id, Aluno=aluno.id)
        for frequencia in frequencias:
            frequencia.delete()

    
class AnoLetivo(models.Model):
    Ano = models.PositiveSmallIntegerField(verbose_name='Ano')
    Data_Inicio = models.DateField(verbose_name='Abertura do ano letivo')
    Data_Fim = models.DateField(verbose_name='Fechamento do ano letivo')
    ABERTO = 'A'
    FECHADO = 'F'
    TIPOS_SITUACAO = (
        (ABERTO,'Aberto'),
        (FECHADO,'Fechado')
    )
    Situacao = models.CharField('Situação', max_length=20, choices=TIPOS_SITUACAO, default=ABERTO)
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

    def checarSituacao(escolaid):
        achou = AnoLetivo.objects.filter(Escola=escolaid, Situacao='A').exists()
        return achou

    def retornar_ativo(escolaid):
        ano = AnoLetivo.objects.filter(Escola=escolaid, Situacao='A')
        if len(ano) == 0:
            return None
        else:
            return ano[0]


class Bimestre(models.Model):
    AnoLetivo = models.ForeignKey('AnoLetivo', on_delete=models.PROTECT, verbose_name='Ano')
    Bimestre = models.DecimalField(max_digits=1, decimal_places=0, verbose_name='Bimestre')
    Data_Inicio = models.DateField(verbose_name='Abertura do bimestre', blank=True, null=True)
    Data_Limite_Notas = models.DateField(verbose_name='Limite do lançamento das Notas',blank=True,null=True)
    Data_Fim = models.DateField(verbose_name='Fechamento do bimestre',blank=True, null=True)
    ABERTO = 'A'
    FECHADO = 'F'
    TIPOS_SITUACAO = (
        (ABERTO,'Aberto'),
        (FECHADO,'Fechado')
    )
    Situacao = models.CharField('Situação', max_length=20, choices=TIPOS_SITUACAO, default=ABERTO)
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
    
    def checarSituacao(idEscola):
        achou = Bimestre.objects.filter(Escola=idEscola, Situacao='A').exists()
        return achou
    
    def gerar_bimestre(ano,idEscola):
        bimestres = Bimestre.objects.filter(Escola=idEscola, AnoLetivo=ano.id).order_by('Bimestre')
        numero = 1
        if len(bimestres) > 0:
            for bimestre in bimestres:
                numero = bimestre.Bimestre
            numero += 1
        return int(numero)

    def retornar_ativo(escolaid):
        bimestre = Bimestre.objects.filter(Escola=escolaid, Situacao='A')
        if len(bimestre) == 0:
            return None
        else:
            return bimestre[0]
                

class Avaliacao(models.Model):
    Nome = models.CharField('Nome',max_length=20)
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola') 


class Nota(models.Model):
    Valor = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Valor')
    Peso = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Peso')
    Nota_Bimestral = models.ForeignKey(
        'Nota_Bimestral', 
        on_delete = models.PROTECT, 
        verbose_name = 'Nota_Bimestral'
    ) 
    Avaliacao = models.ForeignKey('Avaliacao', on_delete = models.PROTECT, verbose_name = 'Avaliacao') 
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola') 


class Nota_Bimestral(models.Model):
    Media = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        verbose_name='Media',
        blank=True, 
        null=True
    )
    Bimestre = models.ForeignKey('Bimestre', on_delete = models.PROTECT, verbose_name = 'Bimestre') 
    Nota_Final = models.ForeignKey('Nota_Final', on_delete = models.PROTECT, verbose_name = 'Nota_Final')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola') 

    def gerar_nota_Bimestral(bimestre, nota_final, escola):
        nota_bimestral = Nota_Bimestral(Bimestre=bimestre, Nota_Final=nota_final, Escola=escola)
        nota_bimestral.save()


class Nota_Final(models.Model):
    Media_Final = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        verbose_name='Media_Final',
        blank=True, 
        null=True
    )
    Matricula_Turma = models.ForeignKey('Matricula_Turma', on_delete = models.PROTECT, verbose_name = 'Matricula_Turma')
    Leciona = models.ForeignKey('Leciona', on_delete = models.PROTECT, verbose_name = 'Leciona')
    AnoLetivo = models.ForeignKey('AnoLetivo', on_delete = models.PROTECT, verbose_name = 'AnoLetivo')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola') 

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['AnoLetivo','Matricula_Turma','Leciona','Escola'], 
                name='unique_Nota_Final'
            )
        ]

    def criar_nota_final(matricula, leciona, ano, escola):
        nota_final = Nota_Final(Matricula_Turma=matricula, Leciona=leciona, AnoLetivo=ano, Escola=escola)
        nota_final.save()
        nota_final = Nota_Final.objects.get(Matricula_Turma=matricula.id, Leciona=leciona.id, AnoLetivo=ano.id, Escola=escola.id)
        bimestre = Bimestre.retornar_ativo(escola.id)
        if bimestre is not None:
            Nota_Bimestral.gerar_nota_Bimestral(bimestre, nota_final, escola)


class Serie(models.Model):
    Numero = models.DecimalField(max_digits=1, decimal_places=0, verbose_name='Numero')
    FUNDAMENTAL = 'F'
    MEDIO = 'M'
    NIVEIS_DE_ESCOLARIDADE = (
        (FUNDAMENTAL,'Ensino Fundamental'),
        (MEDIO,'Ensino Médio')
    )
    Nivel_Escolaridade = models.CharField(
        'Nível Escolaridade',
        max_length=20, 
        choices=NIVEIS_DE_ESCOLARIDADE,
        default=FUNDAMENTAL
    )
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')   

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Numero','Nivel_Escolaridade','Escola'], 
                name='unique_Serie_NVE_Escola'
            )
        ]

    def __str__(self):
        return str(self.Numero) + ' - ' + self.Nivel_Escolaridade

    def gerar_series(nivel,escola):
        if nivel == 'F':
            Serie.gerar_series_fundamental(escola)
        elif nivel == 'M':
            Serie.gerar_series_medio(escola)
        elif nivel == 'FM':
            Serie.gerar_series_fundamental(escola)
            Serie.gerar_series_medio(escola)

    def gerar_series_fundamental(escola):
        for i in range(1,10):
            serie = Serie(Numero=i, Nivel_Escolaridade='F', Escola=escola)
            serie.save()
    
    def gerar_series_medio(escola):
        for i in range(1,4):
            serie = Serie(Numero=i, Nivel_Escolaridade='M', Escola=escola)
            serie.save()

        
class Matriz_Item(models.Model):
    Serie = models.ForeignKey('Serie', on_delete = models.PROTECT, verbose_name = 'Serie') 
    Disciplina = models.ForeignKey('Disciplina', on_delete = models.PROTECT, verbose_name = 'Disciplina') 
    Carga = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Carga')
    Escola = models.ForeignKey('Escola', on_delete = models.PROTECT, verbose_name = 'Escola')  

    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=['Serie','Disciplina','Escola'], 
            name='unique_Serie_Disciplina_Escola'
        )
    ]

    def __str__(self):
        return str(self.Serie.Numero)+' - '+self.Serie.Nivel_Escolaridade+' - '+self.Disciplina.Nome
