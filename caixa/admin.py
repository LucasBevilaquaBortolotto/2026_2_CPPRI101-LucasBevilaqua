from django.contrib import admin
from .models import Caixa, Transacao, CompraVendaFilme


class TransacaoInline(admin.TabularInline):
    model = Transacao
    extra = 0
    readonly_fields = ('valor', 'data', 'descricao', 'tipo')


@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_abrir', 'data_fechar', 'saldo_inicial', 'saldo_final', 'esta_aberto_display')
    list_filter = ('data_abrir',)
    search_fields = ('id',)
    inlines = [TransacaoInline]
    list_per_page = 20

    def esta_aberto_display(self, obj):
        return "Aberto" if obj.esta_aberto else "Fechado"
    esta_aberto_display.short_description = 'Status'


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'caixa', 'data', 'descricao', 'tipo', 'valor')
    list_filter = ('tipo', 'data', 'caixa')
    search_fields = ('descricao',)
    list_per_page = 20
    date_hierarchy = 'data'


@admin.register(CompraVendaFilme)
class CompraVendaFilmeAdmin(admin.ModelAdmin):
    list_display = ('id', 'filme', 'tipo', 'quantidade', 'valor', 'data', 'fornecedor')
    list_filter = ('tipo', 'data')
    search_fields = ('filme__titulo', 'fornecedor')
    list_per_page = 20