from django.urls import path
from .views import (
    CaixaListView, CaixaCreateView, CaixaUpdateView, CaixaDeleteView, CaixaDetailView,
    TransacaoListView, TransacaoCreateView, TransacaoUpdateView, TransacaoDeleteView,
    CompraVendaListView, CompraVendaCreateView, CompraVendaUpdateView, CompraVendaDeleteView, CaixaFecharView
)

urlpatterns = [
    # Caixas
    path('caixas/', CaixaListView.as_view(), name='caixas'),
    path('caixas/novo/', CaixaCreateView.as_view(), name='caixa_novo'),
    path('caixas/editar/<int:pk>/', CaixaUpdateView.as_view(), name='caixa_editar'),
    path('caixas/excluir/<int:pk>/', CaixaDeleteView.as_view(), name='caixa_excluir'),
    path('caixas/<int:pk>/', CaixaDetailView.as_view(), name='caixa_detalhe'),
    path('caixas/<int:pk>/fechar/', CaixaFecharView.as_view(), name='caixa_fechar'),

    # Transações
    path('transacoes/', TransacaoListView.as_view(), name='transacoes'),
    path('transacoes/nova/', TransacaoCreateView.as_view(), name='transacao_nova'),
    path('transacoes/editar/<int:pk>/', TransacaoUpdateView.as_view(), name='transacao_editar'),
    path('transacoes/excluir/<int:pk>/', TransacaoDeleteView.as_view(), name='transacao_excluir'),

    # Compras / Vendas
    path('compras-vendas/', CompraVendaListView.as_view(), name='compras_vendas'),
    path('compras-vendas/nova/', CompraVendaCreateView.as_view(), name='compra_venda_nova'),
    path('compras-vendas/editar/<int:pk>/', CompraVendaUpdateView.as_view(), name='compra_venda_editar'),
    path('compras-vendas/excluir/<int:pk>/', CompraVendaDeleteView.as_view(), name='compra_venda_excluir'),
]