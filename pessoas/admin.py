from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Funcionario


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'documento', 'ativo', 'data_cadastro', 'foto_tag')
    list_filter = ('ativo', 'data_cadastro')
    search_fields = ('nome', 'email', 'documento')
    readonly_fields = ('foto_tag',)
    list_per_page = 20

    def foto_tag(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.foto.url)
        return "-"
    foto_tag.short_description = 'Foto'


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cargo', 'data_admissao', 'foto_tag')
    list_filter = ('cargo', 'data_admissao')
    search_fields = ('nome', 'email', 'cargo')
    readonly_fields = ('foto_tag',)
    list_per_page = 20

    def foto_tag(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.foto.url)
        return "-"
    foto_tag.short_description = 'Foto'