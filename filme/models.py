from django.db import models



class Filme(models.Model):
    titulo = models.CharField('Titulos',max_length=100, help_text='Titulo do Filme')
    genero = models.CharField('Genero',max_length=100, help_text='Genero do Filme')
    anoLançamento = models.CharField('AnoLançamento',max_length=12, help_text='Ano de lançamento do Filme')
    valor = models.CharField('Valor',max_length=4, help_text='Valor do Filme')

    class Meta:
        verbose_name = 'Filme'
        verbose_name_plural = 'Filmes'

    def __str__(self):
        return self.titulo
