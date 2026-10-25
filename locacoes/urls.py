from django.urls import path
from .views import (
    LocacaoListView, LocacaoCreateView, LocacaoUpdateView, LocacaoDeleteView, LocacaoDetailView,
    MultaListView, MultaCreateView, MultaUpdateView, MultaDeleteView, LocacaoDevolverView
)

urlpatterns = [
    # Locações
    path('locacoes/', LocacaoListView.as_view(), name='locacoes'),
    path('locacoes/nova/', LocacaoCreateView.as_view(), name='locacao_nova'),
    path('locacoes/editar/<int:pk>/', LocacaoUpdateView.as_view(), name='locacao_editar'),
    path('locacoes/excluir/<int:pk>/', LocacaoDeleteView.as_view(), name='locacao_excluir'),
    path('locacoes/<int:pk>/', LocacaoDetailView.as_view(), name='locacao_detalhe'),
    path('locacoes/<int:pk>/devolver/', LocacaoDevolverView.as_view(), name='locacao_devolver'),

    # Multas
    path('multas/', MultaListView.as_view(), name='multas'),
    path('multas/nova/', MultaCreateView.as_view(), name='multa_nova'),
    path('multas/editar/<int:pk>/', MultaUpdateView.as_view(), name='multa_editar'),
    path('multas/excluir/<int:pk>/', MultaDeleteView.as_view(), name='multa_excluir'),
]