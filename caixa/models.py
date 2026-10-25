from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from filmes.models import Filme


class Caixa(models.Model):
    data_abrir = models.DateField(verbose_name='Data de Abertura')
    data_fechar = models.DateField(null=True, blank=True, verbose_name='Data de Fechamento')
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Saldo Inicial')
    saldo_final = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Saldo Final')

    class Meta:
        verbose_name = 'Caixa'
        verbose_name_plural = 'Caixas'
        ordering = ['-data_abrir']

    def __str__(self):
        status = "Aberto" if self.data_fechar is None else "Fechado"
        return f'Caixa #{self.id} - {self.data_abrir.strftime("%d/%m/%Y")} ({status})'

    @property
    def esta_aberto(self):
        return self.data_fechar is None

    def calcular_totais(self):

        transacoes = self.transacoes.all()
        total_entradas = transacoes.filter(tipo='E').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        total_saidas = transacoes.filter(tipo='S').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        saldo_atual = self.saldo_inicial + total_entradas - total_saidas
        return total_entradas, total_saidas, saldo_atual

    def fechar(self):

        if not self.esta_aberto:
            raise ValueError('Este caixa já está fechado.')

        total_entradas, total_saidas, saldo_atual = self.calcular_totais()

        self.data_fechar = timezone.now().date()
        self.saldo_final = saldo_atual
        self.save()

        return total_entradas, total_saidas, saldo_atual


class Transacao(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]

    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, related_name='transacoes', verbose_name='Caixa')
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor')
    data = models.DateField(verbose_name='Data')
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, verbose_name='Tipo')

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-id']

    def __str__(self):
        tipo = "Entrada" if self.tipo == 'E' else "Saída"
        return f'{tipo} - R$ {self.valor} ({self.descricao})'


class CompraVendaFilme(models.Model):
    TIPO_CHOICES = [
        ('C', 'Compra'),
        ('V', 'Venda'),
    ]

    transacao = models.ForeignKey(Transacao, on_delete=models.CASCADE, related_name='compras_vendas', verbose_name='Transação')
    filme = models.ForeignKey(Filme, on_delete=models.PROTECT, related_name='compras_vendas', verbose_name='Filme')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Unitário')
    data = models.DateField(verbose_name='Data')
    fornecedor = models.CharField(max_length=100, blank=True, null=True, verbose_name='Fornecedor')
    quantidade = models.PositiveIntegerField(default=1, verbose_name='Quantidade')
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, verbose_name='Tipo (Compra/Venda)')

    class Meta:
        verbose_name = 'Compra/Venda de Filme'
        verbose_name_plural = 'Compras/Vendas de Filmes'
        ordering = ['-data']

    def __str__(self):
        tipo = "Compra" if self.tipo == 'C' else "Venda"
        return f'{tipo} - {self.filme.titulo} (x{self.quantidade})'

    def atualizar_estoque(self, reverter=False):

        filme = self.filme

        if self.tipo == 'C':  # Compra
            if reverter:
                filme.estoque -= self.quantidade
            else:
                filme.estoque += self.quantidade
        else:
            if reverter:
                filme.estoque += self.quantidade
            else:
                filme.estoque -= self.quantidade


        if filme.estoque < 0:
            filme.estoque = 0

        filme.disponivel = filme.estoque > 0
        filme.save()