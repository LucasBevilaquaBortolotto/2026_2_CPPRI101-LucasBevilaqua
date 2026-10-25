from decimal import Decimal

from django.db import models
from django.utils import timezone

from pessoas.models import Cliente, Funcionario
from filmes.models import Filme


class Locacao(models.Model):
    STATUS_CHOICES = [
        ('A', 'Aberta'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='locacoes', verbose_name='Cliente')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='locacoes', verbose_name='Funcionário')
    data_locacao = models.DateField(verbose_name='Data da Locação')
    data_devolucao = models.DateField(verbose_name='Data Prevista de Devolução')
    real_data_devolucao = models.DateField(null=True, blank=True, verbose_name='Data Real de Devolução')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Total')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A', verbose_name='Status')
    multa_aplicada = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Multa Aplicada')

    filmes = models.ManyToManyField(Filme, through='LocacaoFilme', related_name='locacoes')

    class Meta:
        verbose_name = 'Locação'
        verbose_name_plural = 'Locações'
        ordering = ['-data_locacao']

    def __str__(self):
        return f'Locação #{self.id} - {self.cliente.nome} ({self.get_status_display()})'

    @property
    def esta_atrasada(self):
        if self.status != 'A':
            return False
        return timezone.now().date() > self.data_devolucao

    @property
    def dias_atraso(self):
        if not self.esta_atrasada:
            return 0
        return (timezone.now().date() - self.data_devolucao).days

    def devolver(self, valor_multa_por_dia=Decimal('5.00')):

        if self.status != 'A':
            raise ValueError('Só é possível devolver locações abertas.')

        hoje = timezone.now().date()
        self.real_data_devolucao = hoje
        self.status = 'F'


        multa_valor = Decimal('0.00')
        dias = 0

        if hoje > self.data_devolucao:
            dias = (hoje - self.data_devolucao).days
            multa_valor = Decimal(dias) * valor_multa_por_dia
            self.multa_aplicada = multa_valor


            Multa.objects.create(
                locacao=self,
                valor=multa_valor,
                dias_atraso=dias,
                status='P'
            )

        self.save()


        for item in self.locacaofilme_set.all():
            filme = item.filme
            filme.estoque += item.quantidade
            filme.disponivel = True
            filme.save()

        return multa_valor, dias


class LocacaoFilme(models.Model):

    locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1, verbose_name='Quantidade')

    class Meta:
        verbose_name = 'Filme da Locação'
        verbose_name_plural = 'Filmes da Locação'
        unique_together = ['locacao', 'filme']

    def __str__(self):
        return f'{self.filme.titulo} (x{self.quantidade})'


class Multa(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('Q', 'Paga'),
        ('C', 'Cancelada'),
    ]

    locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='multas', verbose_name='Locação')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor da Multa')
    dias_atraso = models.PositiveIntegerField(verbose_name='Dias de Atraso')
    data_geracao = models.DateField(auto_now_add=True, verbose_name='Data de Geração')
    data_pagamento = models.DateField(null=True, blank=True, verbose_name='Data de Pagamento')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', verbose_name='Status')

    class Meta:
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'
        ordering = ['-data_geracao']

    def __str__(self):
        return f'Multa #{self.id} - Locação {self.locacao.id} - R$ {self.valor}'