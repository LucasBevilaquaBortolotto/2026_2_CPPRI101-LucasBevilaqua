from django.contrib import admin
from django.utils.html import format_html
from .models import Filme


@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'genero', 'ano_lancamento', 'class_etaria', 'valor', 'estoque', 'disponivel', 'capa_tag')
    list_filter = ('genero', 'disponivel', 'class_etaria', 'ano_lancamento')
    search_fields = ('titulo', 'genero')
    list_editable = ('estoque', 'disponivel', 'valor')
    readonly_fields = ('capa_tag',)
    list_per_page = 20

    def capa_tag(self, obj):
        if obj.capa:
            return format_html('<img src="{}" width="60" height="80" style="object-fit: cover;" />', obj.capa.url)
        return "-"
    capa_tag.short_description = 'Capa'