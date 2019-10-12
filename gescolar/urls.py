from django.contrib import admin
from django.urls import path, include
from gestaoEscolar.views import inicio

urlpatterns = [
    path('', inicio.gestao_escolar_inicio , name='gestao_escolar_inicio'),
    path('admin/', admin.site.urls),
    path('gestaoEscolar/', include('gestaoEscolar.urls'))
]
