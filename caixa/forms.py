from django import forms
from .models import Caixa, Transacao, CompraVendaFilme


class CaixaModelForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['data_abrir', 'saldo_inicial']
        widgets = {
            'data_abrir': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'data_abrir': {'required': 'A data de abertura é obrigatória.'},
            'saldo_inicial': {'required': 'O saldo inicial é obrigatório.'},
        }


class TransacaoModelForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['caixa', 'valor', 'data', 'descricao', 'tipo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'caixa': {'required': 'Selecione o caixa.'},
            'valor': {'required': 'O valor é obrigatório.'},
            'data': {'required': 'A data é obrigatória.'},
            'descricao': {'required': 'A descrição é obrigatória.'},
            'tipo': {'required': 'Selecione o tipo da transação.'},
        }


class CompraVendaFilmeModelForm(forms.ModelForm):
    class Meta:
        model = CompraVendaFilme
        fields = ['transacao', 'filme', 'tipo', 'quantidade', 'valor', 'data', 'fornecedor']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'quantidade': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'tipo': 'Tipo (Compra ou Venda)',
            'valor': 'Valor Unitário',
        }