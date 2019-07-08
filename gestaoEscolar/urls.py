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



]