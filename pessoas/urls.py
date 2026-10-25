from django.urls import path
from .views import (
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    FuncionarioListView, FuncionarioCreateView, FuncionarioUpdateView, FuncionarioDeleteView
)

urlpatterns = [
    # Clientes
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('clientes/novo/', ClienteCreateView.as_view(), name='cliente_novo'),
    path('clientes/editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/excluir/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_excluir'),

    # Funcionários
    path('funcionarios/', FuncionarioListView.as_view(), name='funcionarios'),
    path('funcionarios/novo/', FuncionarioCreateView.as_view(), name='funcionario_novo'),
    path('funcionarios/editar/<int:pk>/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionarios/excluir/<int:pk>/', FuncionarioDeleteView.as_view(), name='funcionario_excluir'),
]