from django.db import models

class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    fone = models.CharField('Telefone', max_length=15, help_text='Número do telefone')
    email = models.EmailField('E-mail', max_length=100, help_text='Endereço de e-mail', unique=True)
    foto = models.ImageField('Foto', upload_to='fotos', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

class Funcionario(Pessoa):
    cargo = models.CharField('Cargo', max_length=35, help_text='Cargo na empresa')
    dataAdmissao = models.DateField('Data de Admissão', help_text='Data de admissão na empresa')
    salario = models.DecimalField('Salário', max_digits=8, decimal_places=2, help_text='Salário do funcionário')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

class Cliente(Pessoa):
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço completo')
    dataCadastro = models.DateField('Data de Cadastro', auto_now_add=True)
    ativo = models.BooleanField('Ativo', default=True)
    documento = models.BooleanField('Documento Apresentado', default=False, help_text='Obrigatório para > 16 anos se necessário')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Filme(models.Model):
    idFilme = models.AutoField(primary_key=True)
    titulo = models.CharField('Título', max_length=100, unique=True, help_text='Título do filme')
    genero = models.CharField('Gênero', max_length=50, help_text='Gênero do filme')
    anoLancamento = models.IntegerField('Ano de Lançamento')
    classEtaria = models.IntegerField('Classificação Etária', help_text='Ex: 0, 10, 12, 14, 16, 18')
    valor = models.DecimalField('Valor da Locação', max_digits=6, decimal_places=2)
    estoque = models.IntegerField('Estoque', default=0)
    disponivel = models.BooleanField('Disponível', default=True)

    class Meta:
        verbose_name = 'Filme'
        verbose_name_plural = 'Filmes'

    def __str__(self):
        return self.titulo

class Locacao(models.Model):
    idLocacao = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name='Cliente')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, verbose_name='Funcionário')
    filmes = models.ManyToManyField(Filme, through='LocacaoFilme', verbose_name='Filmes')
    dataLocacao = models.DateField('Data da Locação', auto_now_add=True)
    dataDevol = models.DateField('Data Prevista Devolução')
    realDataDevol = models.DateField('Real Data de Devolução', null=True, blank=True)
    valor = models.DecimalField('Valor Total', max_digits=8, decimal_places=2, default=0.0)
    status = models.CharField('Status', max_length=30, default='Aberta')
    multaAplicada = models.DecimalField('Multa Aplicada', max_digits=8, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = 'Locação'
        verbose_name_plural = 'Locações'

class LocacaoFilme(models.Model):
    locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

class Multa(models.Model):
    idMulta = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name='Cliente')
    locacao = models.ForeignKey(Locacao, on_delete=models.PROTECT, verbose_name='Locação')
    valor = models.DecimalField('Valor da Multa', max_digits=8, decimal_places=2)
    diasAtraso = models.IntegerField('Dias de Atraso')
    dataGeracao = models.DateField('Data de Geração', auto_now_add=True)
    dataPagamento = models.DateField('Data de Pagamento', null=True, blank=True)
    status = models.CharField('Status', max_length=20, default='Pendente')

    class Meta:
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'

class Caixa(models.Model):
    idCaixa = models.AutoField(primary_key=True)
    dataAbrir = models.DateField('Data de Abertura')
    dataFechar = models.DateField('Data de Fechamento', null=True, blank=True)
    saldoInicial = models.DecimalField('Saldo Inicial', max_digits=10, decimal_places=2)
    saldoFinal = models.DecimalField('Saldo Final', max_digits=10, decimal_places=2, default=0.0)

class Transacao(models.Model):
    id = models.AutoField(primary_key=True)
    caixa = models.ForeignKey(Caixa, on_delete=models.PROTECT)
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)
    data = models.DateField('Data', auto_now_add=True)
    descricao = models.CharField('Descrição', max_length=200)
    tipo = models.CharField('Tipo', max_length=20)

class CompraVendaFilmes(models.Model):
    id = models.AutoField(primary_key=True)
    transacao = models.ForeignKey(Transacao, on_delete=models.PROTECT)
    filme = models.ForeignKey(Filme, on_delete=models.PROTECT)
    valor = models.DecimalField('Valor Unitário', max_digits=8, decimal_places=2)
    quantidade = models.IntegerField('Quantidade')
    fonecedor = models.CharField('Fornecedor', max_length=100)
    data = models.DateField('Data', auto_now_add=True)