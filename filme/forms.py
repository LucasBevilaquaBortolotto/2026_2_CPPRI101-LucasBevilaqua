from django import forms
from .models import Filme

class FilmeForm(forms.ModelForm):
    class Meta:
        model = Filme
        fields = '__all__'


        error_messages = {
            'titulo':{'required': 'O titulos é um campo obrigatoro'},
            'genero':{'required':'O genero é um campo obrigatoro'},
            'anoLançamento':{'required':'A data de lançamento é um campo obrigatoro'},
            'valor':{'required':'O valor é um campo obrigatoro'},
        }