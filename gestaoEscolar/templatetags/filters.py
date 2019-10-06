from django import template
from datetime import datetime

register = template.Library()

@register.filter
def numero_decimal(valor):
    return str(valor).replace(',','.')

@register.filter
def data_retorno(valor):
    return str(valor)

@register.filter
def tira_lista(valor):
    return str(valor).replace('<ul class="errorlist"><li>', '').replace('<ul class="errorlist nonfield"><li>', '').replace('</li></ul>', '')
