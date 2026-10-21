from django import forms
from django.core.exceptions import ValidationError
from .models import Locacao, Multa, Cliente, Funcionario, Transacao, Caixa
from datetime import date


class LocacaoModelForm(forms.ModelForm):
    class Meta:
        model = Locacao
        fields = ['cliente', 'funcionario', 'filmes', 'dataDevol']

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        filmes = cleaned_data.get('filmes')

        if cliente:
            # Regra: Pendência (Multa pendente)
            multas_pendentes = Multa.objects.filter(cliente=cliente, status='Pendente').exists()
            if multas_pendentes:
                raise ValidationError("O cliente possui multas pendentes e não pode realizar novas locações.")

            # Regra: Limite de locação (Máximo 3 filmes ativos)
            locacoes_ativas = Locacao.objects.filter(cliente=cliente, status='Aberta')
            total_filmes_ativos = sum([l.filmes.count() for l in locacoes_ativas])
            if filmes and (total_filmes_ativos + len(filmes) > 3):
                raise ValidationError(
                    "Limite excedido: O cliente pode ter no máximo 3 filmes alugados simultaneamente.")

        if filmes:
            for filme in filmes:
                # Regra: Disponibilidade
                if not filme.disponivel or filme.estoque <= 0:
                    raise ValidationError(f"O filme '{filme.titulo}' não está disponível para locação.")

                # Regra: Restrição de Idade (> 16 requer documento)
                if filme.classEtaria > 16 and cliente and not cliente.documento:
                    raise ValidationError(
                        f"O filme '{filme.titulo}' exige classificação etária maior que 16 e o cliente não apresentou documento.")

        return cleaned_data

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'fone', 'email', 'foto', 'endereco', 'documento', 'ativo']
        widgets = {
            'endereco': forms.TextInput(attrs={'placeholder': 'Endereço completo'}),
        }

class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'fone', 'email', 'foto', 'cargo', 'dataAdmissao', 'salario']
        widgets = {
            'dataAdmissao': forms.DateInput(attrs={'type': 'date'}),
        }


class LocacaoUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Locacao
        fields = ['cliente', 'funcionario', 'filmes', 'dataDevol', 'status', 'realDataDevol']
        widgets = {
            'dataDevol': forms.DateInput(attrs={'type': 'date'}),
            'realDataDevol': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        locacao = super().save(commit=False)

        # Se o status foi alterado para 'Devolvida' e não há data real informada, define a data de hoje
        if locacao.status == 'Devolvida' and not locacao.realDataDevol:
            locacao.realDataDevol = date.today()

            # Atualiza o estoque dos filmes devolvidos
            for filme in locacao.filmes.all():
                filme.estoque += 1
                filme.disponivel = True
                filme.save()

        if commit:
            locacao.save()
            self.save_m2m()
        return locacao

class MultaModelForm(forms.ModelForm):
    class Meta:
        model = Multa
        fields = ['cliente', 'locacao', 'valor', 'diasAtraso', 'status', 'dataPagamento']
        widgets = {
            'dataPagamento': forms.DateInput(attrs={'type': 'date'}),
        }

class TransacaoModelForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['caixa', 'funcionario', 'tipo', 'descricao', 'valor']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class CaixaModelForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['saldoInicial', 'status']

class CaixaUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['saldoInicial', 'saldoFinal', 'dataFechamento', 'status']
        widgets = {
            'dataFechamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }