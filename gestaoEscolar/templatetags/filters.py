from django import template

register = template.Library()

@register.filter
def numero_decimal(valor):
    return str(valor).replace(',','.')