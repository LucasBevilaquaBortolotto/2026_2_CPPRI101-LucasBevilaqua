from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    telefone = models.CharField(max_length=15, verbose_name='Telefone')
    email = models.EmailField(max_length=100, verbose_name='E-mail')
    endereco = models.CharField(max_length=200, verbose_name='Endereço')
    foto = models.ImageField(upload_to='pessoas/', null=True, blank=True, verbose_name='Foto')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class Cliente(Pessoa):
    data_cadastro = models.DateField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    documento = models.BooleanField(default=False, verbose_name='Documento Entregue')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Funcionario(Pessoa):
    cargo = models.CharField(max_length=50, verbose_name='Cargo')
    data_admissao = models.DateField(verbose_name='Data de Admissão')
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salário')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} - {self.cargo}'