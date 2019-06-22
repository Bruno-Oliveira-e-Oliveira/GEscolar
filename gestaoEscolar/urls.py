from django.urls import path, include
from .views import escola_novo

urlpatterns = [
    path('escola/novo', escola_novo, name='escola_novo')
]