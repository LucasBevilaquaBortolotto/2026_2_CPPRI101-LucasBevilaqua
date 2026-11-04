from django import forms
from django.core.exceptions import ValidationError
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

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if cliente:
            # Regra 5: Cliente com multa pendente não pode alugar
            tem_pendencia = Multa.objects.filter(
                locacao__cliente=cliente,
                status='P'
            ).exists()
            if tem_pendencia:
                raise ValidationError('Este cliente possui multas pendentes e não pode realizar novas locações.')
        return cliente


class LocacaoFilmeForm(forms.ModelForm):
    class Meta:
        model = LocacaoFilme
        fields = ['filme', 'quantidade']
        widgets = {
            'filme': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_filme(self):
        filme = self.cleaned_data.get('filme')
        if filme:
            # Regra 4: Filme precisa estar disponível
            if not filme.disponivel or filme.estoque <= 0:
                raise ValidationError(f'O filme "{filme.titulo}" não está disponível para locação.')
        return filme

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        filme = self.cleaned_data.get('filme')
        if filme and quantidade:
            if quantidade > filme.estoque:
                raise ValidationError(f'Estoque insuficiente. Disponível: {filme.estoque}')
        return quantidade



LocacaoFilmeFormSet = inlineformset_factory(
    Locacao,
    LocacaoFilme,
    form=LocacaoFilmeForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=3,          # Regra 1: Máximo 3 filmes
)


class MultaModelForm(forms.ModelForm):
    class Meta:
        model = Multa
        fields = ['locacao', 'valor', 'dias_atraso', 'data_pagamento', 'status']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        }