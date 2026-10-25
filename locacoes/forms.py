from django import forms
from django.forms import inlineformset_factory
from .models import Locacao, LocacaoFilme, Multa
from filmes.models import Filme


class LocacaoModelForm(forms.ModelForm):
    class Meta:
        model = Locacao
        fields = ['cliente', 'funcionario', 'data_locacao', 'data_devolucao', 'status']
        widgets = {
            'data_locacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class LocacaoFilmeForm(forms.ModelForm):
    class Meta:
        model = LocacaoFilme
        fields = ['filme', 'quantidade']
        widgets = {
            'filme': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }



LocacaoFilmeFormSet = inlineformset_factory(
    Locacao,
    LocacaoFilme,
    form=LocacaoFilmeForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class MultaModelForm(forms.ModelForm):
    class Meta:
        model = Multa
        fields = ['locacao', 'valor', 'dias_atraso', 'data_pagamento', 'status']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        }