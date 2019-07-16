from django.urls import path, include
from .views import *

urlpatterns = [
    path('', gestao_escolar_inicio , name='gestao_escolar_inicio'),
    path('login/', login , name='login'),
    path('logout/', logout , name='logout'),

    path('diretor/novo/', diretor_novo, name='diretor_novo'),

    path('escola/novo/', escola_novo, name='escola_novo'),
    path('escola/alterar/<int:id>', escola_alterar, name='escola_alterar'),

    path('secretarios/', secretario_listagem, name='secretario_listagem'),
    path('secretario/novo/', secretario_novo, name='secretario_novo'),
    path('secretario/alterar/<int:id>', secretario_alterar, name='secretario_alterar'),
    path('secretario/<int:id>', secretario_consultar, name='secretario_consultar'),
    path('secretario/deletar/<int:id>', secretario_deletar, name='secretario_deletar'),

    path('professores/', professor_listagem, name='professor_listagem'),
    path('professor/novo/', professor_novo, name='professor_novo'),
    path('professor/alterar/<int:id>', professor_alterar, name='professor_alterar'),
    path('professor/<int:id>', professor_consultar, name='professor_consultar'),
    path('professor/deletar/<int:id>', professor_deletar, name='professor_deletar'),

    path('alunos/', aluno_listagem, name='aluno_listagem'),
    path('aluno/novo/', aluno_novo, name='aluno_novo'),
    path('aluno/alterar/<int:id>', aluno_alterar, name='aluno_alterar'),
    path('aluno/<int:id>', aluno_consultar, name='aluno_consultar'),
    path('aluno/deletar/<int:id>', aluno_deletar, name='aluno_deletar'),

    path('anos/', ano_listagem, name='ano_listagem'),
    path('ano/novo/', ano_novo, name='ano_novo'),
    path('ano/alterar/<int:id>', ano_alterar, name='ano_alterar'),
    path('ano/<int:id>', ano_consultar, name='ano_consultar'),
    path('ano/deletar/<int:id>', ano_deletar, name='ano_deletar'),

]