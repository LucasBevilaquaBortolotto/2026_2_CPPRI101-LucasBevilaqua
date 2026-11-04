from django.contrib import admin
from .models import Locacao, LocacaoFilme, Multa


class LocacaoFilmeInline(admin.TabularInline):
    model = LocacaoFilme
    extra = 1


@admin.register(Locacao)
class LocacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'funcionario', 'data_locacao', 'data_devolucao', 'valor', 'status', 'multa_aplicada')
    list_filter = ('status', 'data_locacao', 'funcionario')
    search_fields = ('cliente__nome', 'funcionario__nome')
    inlines = [LocacaoFilmeInline]
    list_per_page = 20
    date_hierarchy = 'data_locacao'


@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'locacao', 'valor', 'dias_atraso', 'data_geracao', 'status')
    list_filter = ('status', 'data_geracao')
    search_fields = ('locacao__cliente__nome',)
    list_per_page = 20