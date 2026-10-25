from django import forms
from .models import Cliente, Funcionario

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'email', 'endereco', 'foto', 'ativo', 'documento']
        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório.'},
            'cpf': {'required': 'O CPF é um campo obrigatório.',
                    'unique': 'Já existe um cliente com este CPF.'},
            'telefone': {'required': 'O telefone é um campo obrigatório.'},
            'email': {'required': 'O e-mail é um campo obrigatório.',
                      'invalid': 'Informe um e-mail válido.'},
        }


class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'telefone', 'email', 'endereco', 'foto', 'cargo', 'data_admissao', 'salario']
        error_messages = {
            'nome': {'required': 'O nome do funcionário é um campo obrigatório.'},
            'cpf': {'required': 'O CPF é um campo obrigatório.',
                    'unique': 'Já existe um funcionário com este CPF.'},
            'cargo': {'required': 'O cargo é um campo obrigatório.'},
            'data_admissao': {'required': 'A data de admissão é um campo obrigatório.'},
            'salario': {'required': 'O salário é um campo obrigatório.'},
        }