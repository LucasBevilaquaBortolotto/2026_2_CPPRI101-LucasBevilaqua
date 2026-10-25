from django.db import models

class Filme(models.Model):
    titulo = models.CharField(max_length=150, verbose_name='Título')
    genero = models.CharField(max_length=50, verbose_name='Gênero')
    ano_lancamento = models.PositiveIntegerField(verbose_name='Ano de Lançamento')
    class_etaria = models.PositiveIntegerField(verbose_name='Classificação Etária')
    valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Valor (locação)')
    estoque = models.PositiveIntegerField(default=0, verbose_name='Estoque')
    disponivel = models.BooleanField(default=True, verbose_name='Disponível')
    capa = models.ImageField(upload_to='filmes/', null=True, blank=True, verbose_name='Capa')

    class Meta:
        verbose_name = 'Filme'
        verbose_name_plural = 'Filmes'
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo} ({self.ano_lancamento})'