from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    inicio, 
    aluno,
    ano,
    aula,
    bimestre,
    disciplina,
    escola,
    gestor,
    inicio,
    login,
    professor,
    secretario,
    turma,
    serie,
    matriz,
    leciona,
    avaliacao,
    relatorios
)

urlpatterns = [
    path('', inicio.gestao_escolar_inicio , name='gestao_escolar_inicio'),
    path('login/', login.login , name='login'),
    path('logout/', login.logout , name='logout'),

    path('diretor/novo/', gestor.diretor_novo, name='diretor_novo'),

    path('escola/novo/', escola.escola_novo, name='escola_novo'),
    path('escola/alterar/<int:id>', escola.escola_alterar, name='escola_alterar'),

    path('secretarios/', secretario.secretario_listagem, name='secretario_listagem'),
    path('secretario/novo/', secretario.secretario_novo, name='secretario_novo'),
    path('secretario/alterar/<int:id>', secretario.secretario_alterar, name='secretario_alterar'),
    path('secretario/<int:id>', secretario.secretario_consultar, name='secretario_consultar'),
    path('secretario/deletar/<int:id>', secretario.secretario_deletar, name='secretario_deletar'),

    path('professores/', professor.professor_listagem, name='professor_listagem'),
    path('professor/novo/', professor.professor_novo, name='professor_novo'),
    path('professor/alterar/<int:id>', professor.professor_alterar, name='professor_alterar'),
    path('professor/<int:id>', professor.professor_consultar, name='professor_consultar'),
    path('professor/deletar/<int:id>', professor.professor_deletar, name='professor_deletar'),

    path('alunos/', aluno.aluno_listagem, name='aluno_listagem'),
    path('aluno/novo/', aluno.aluno_novo, name='aluno_novo'),
    path('aluno/alterar/<int:id>', aluno.aluno_alterar, name='aluno_alterar'),
    path('aluno/<int:id>', aluno.aluno_consultar, name='aluno_consultar'),
    path('aluno/deletar/<int:id>', aluno.aluno_deletar, name='aluno_deletar'),

    path('anos/', ano.ano_listagem, name='ano_listagem'),
    path('ano/novo/', ano.ano_novo, name='ano_novo'),
    path('ano/alterar/<int:id>', ano.ano_alterar, name='ano_alterar'),
    path('ano/<int:id>', ano.ano_consultar, name='ano_consultar'),
    path('ano/deletar/<int:id>', ano.ano_deletar, name='ano_deletar'),

    path('ano/<int:idA>/bimestres/', bimestre.bimestre_listagem, name='bimestre_listagem'),
    path('ano/<int:idA>/bimestre/novo/', bimestre.bimestre_novo, name='bimestre_novo'),
    path('ano/<int:idA>/bimestre/alterar/<int:idB>', bimestre.bimestre_alterar, name='bimestre_alterar'),
    path('ano/<int:idA>/bimestre/<int:idB>', bimestre.bimestre_consultar, name='bimestre_consultar'),
    path('ano/<int:idA>/bimestre/deletar/<int:idB>', bimestre.bimestre_deletar, name='bimestre_deletar'),

    path('disciplinas/', disciplina.disciplina_listagem, name='disciplina_listagem'),
    path('disciplina/novo/', disciplina.disciplina_novo, name='disciplina_novo'),
    path('disciplina/alterar/<int:id>', disciplina.disciplina_alterar, name='disciplina_alterar'),
    path('disciplina/<int:id>', disciplina.disciplina_consultar, name='disciplina_consultar'),
    path('disciplina/deletar/<int:id>', disciplina.disciplina_deletar, name='disciplina_deletar'),

    path('turmas/', turma.turma_listagem, name='turma_listagem'),
    path('turma/novo/', turma.turma_novo, name='turma_novo'),
    path('turma/alterar/<int:id>', turma.turma_alterar, name='turma_alterar'),
    path('turma/<int:id>', turma.turma_consultar, name='turma_consultar'),
    path('turma/deletar/<int:id>', turma.turma_deletar, name='turma_deletar'),

    path('turma/<int:idT>/gestao/',turma.gerenciamento_turma_listagem,name='gerenciamento_turma_listagem'),
    path('turma/<int:idT>/gestao/matricula/novo',turma.matricula_turma_novo,name='matricula_turma_novo'),
    path('turma/<int:idT>/gestao/matricula/alterar/<int:idM>', turma.matricula_turma_alterar, name='matricula_turma_alterar'),
    path('turma/<int:idT>/gestao/matricula/<int:idM>', turma.matricula_turma_consultar, name='matricula_turma_consultar'),
    path('turma/<int:idT>/gestao/matricula/deletar/<int:idM>', turma.matricula_turma_deletar, name='matricula_turma_deletar'),

    path('turma/<int:idT>/gestao/lecionas/',leciona.leciona_listagem,name='leciona_listagem'),
    path('turma/<int:idT>/gestao/leciona/alterar/<int:idL>', leciona.leciona_alterar, name='leciona_alterar'),
    path('turma/<int:idT>/gestao/leciona/<int:idL>', leciona.leciona_consultar, name='leciona_consultar'),

    path('turma/<int:idT>/gestao/avaliacoes/',avaliacao.avaliacao_listagem,name='avaliacao_listagem'),
    path('turma/<int:idT>/gestao/avaliacao/novo/',avaliacao.avaliacao_novo,name='avaliacao_novo'),
    path('turma/<int:idT>/gestao/avaliacao/alterar/<int:idAv>',avaliacao.avaliacao_alterar,name='avaliacao_alterar'),
    path('turma/<int:idT>/gestao/avaliacao/<int:idAv>',avaliacao.avaliacao_consultar,name='avaliacao_consultar'),
    path('turma/<int:idT>/gestao/avaliacao/deletar/<int:idAv>',avaliacao.avaliacao_deletar,name='avaliacao_deletar'),

    path('turma/<int:idT>/aulas/', aula.aula_listagem, name='aula_listagem'),
    # path('ajax/aulas/', aula.aula_listagem_ajax, name='aula_listagem_ajax'),
    path('turma/<int:idT>/aula/novo/', aula.aula_novo, name='aula_novo'),
    path('turma/<int:idT>/aula/alterar/<int:idA>', aula.aula_alterar, name='aula_alterar'),
    path('turma/<int:idT>/aula/<int:idA>', aula.aula_consultar, name='aula_consultar'),
    path('turma/<int:idT>/aula/deletar/<int:idA>', aula.aula_deletar, name='aula_deletar'),
    path('turma/<int:idT>/aula/<int:idA>/chamada', aula.lista_chamada, name='lista_chamada'),

    path('series/', serie.serie_listagem, name='serie_listagem'),
    path('serie/<int:id>/matriz/', matriz.matriz_item_listagem, name='matriz_item_listagem'),
    path('serie/<int:idS>/matriz/novo/', matriz.matriz_item_novo, name='matriz_item_novo'),
    path('serie/<int:idS>/matriz/alterar/<int:idM>', matriz.matriz_item_alterar, name='matriz_item_alterar'),
    path('serie/<int:idS>/matriz/<int:idM>', matriz.matriz_item_consultar, name='matriz_item_consultar'),
    path('serie/<int:idS>/matriz/deletar/<int:idM>', matriz.matriz_item_deletar, name='matriz_item_deletar'),

    path('turma/<int:idT>/gestao/matricula/<int:idM>/relatorio/',relatorios.relatorio_notas_frequencias,name='relatorio_notas_frequencias'),
    


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)