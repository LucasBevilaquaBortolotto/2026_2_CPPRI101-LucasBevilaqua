from django import forms
from .models import Filme

class FilmeModelForm(forms.ModelForm):
    class Meta:
        model = Filme
        fields = ['titulo', 'genero', 'ano_lancamento', 'class_etaria', 'valor', 'estoque', 'disponivel', 'capa']
        error_messages = {
            'titulo': {'required': 'O título do filme é obrigatório.'},
            'genero': {'required': 'O gênero é obrigatório.'},
            'ano_lancamento': {'required': 'O ano de lançamento é obrigatório.'},
            'class_etaria': {'required': 'A classificação etária é obrigatória.'},
            'valor': {'required': 'O valor da locação é obrigatório.'},
            'estoque': {'required': 'A quantidade em estoque é obrigatória.'},
        }