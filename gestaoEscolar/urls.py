from django.urls import path, include
from .views import (
    inicio, 
    aluno,
    ano,
    bimestre,
    escola,
    gestor,
    inicio,
    login,
    professor,
    secretario,

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
]