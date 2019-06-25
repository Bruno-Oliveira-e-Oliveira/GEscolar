from django.urls import path, include
from .views import gestao_escolar_inicio, login, logout, escola_novo

urlpatterns = [
    path('', gestao_escolar_inicio , name='gestao_escolar_inicio'),
    path('login/', login , name='login'),
    path('logout/', logout , name='logout'),





    path('escola/novo', escola_novo, name='escola_novo')
]