from django.contrib import admin
from .models import (
    Escola,
    Telefone,
    Endereco,
)

# Register your models here.

admin.site.register(Escola)
admin.site.register(Telefone)
admin.site.register(Endereco)