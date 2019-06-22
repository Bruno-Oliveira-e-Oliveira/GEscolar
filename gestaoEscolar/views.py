from django.shortcuts import render
from .forms import EscolaForm

# Create your views here.

def escola_novo(request):
    escola = EscolaForm()
    return render(request,'escola/escola_form.html',{'form':escola})