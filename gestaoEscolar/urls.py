from django.urls import path, include
from .views import gestao_escolar_inicio, login, logout, diretor_novo, escola_novo

urlpatterns = [
    path('', gestao_escolar_inicio , name='gestao_escolar_inicio'),
    path('login/', login , name='login'),
    path('logout/', logout , name='logout'),
    path('diretor/novo/', diretor_novo, name='diretor_novo'),





    path('escola/novo', escola_novo, name='escola_novo')
]