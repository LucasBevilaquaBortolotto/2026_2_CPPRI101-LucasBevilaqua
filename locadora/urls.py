from django.urls import path
from .views import (
    HomeView, FilmesView, FilmeAddView, FilmeUpdateView, FilmeDeleteView,
    LocacoesView, LocacaoAddView, LocacaoUpdateView, ClientesView, ClienteAddView, ClienteUpdateView,
    FuncionariosView, FuncionarioAddView, FuncionarioUpdateView, FuncionarioDeleteView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # Filmes
    path('filmes/', FilmesView.as_view(), name='filmes'),
    path('filmes/novo/', FilmeAddView.as_view(), name='filme_adicionar'),
    path('filmes/<int:pk>/editar/', FilmeUpdateView.as_view(), name='filme_editar'),
    path('filmes/<int:pk>/apagar/', FilmeDeleteView.as_view(), name='filme_apagar'),

    # Locações
    path('locacoes/', LocacoesView.as_view(), name='locacoes'),
    path('locacoes/nova/', LocacaoAddView.as_view(), name='locacao_adicionar'),
    path('locacoes/<int:pk>/editar/', LocacaoUpdateView.as_view(), name='locacao_editar'),

    # Clientes
    path('clientes/', ClientesView.as_view(), name='clientes'),
    path('clientes/novo/', ClienteAddView.as_view(), name='cliente_adicionar'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_editar'),

    # Funcionários
    path('funcionarios/', FuncionariosView.as_view(), name='funcionarios'),
    path('funcionarios/novo/', FuncionarioAddView.as_view(), name='funcionario_adicionar'),
    path('funcionarios/<int:pk>/editar/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionarios/<int:pk>/apagar/', FuncionarioDeleteView.as_view(), name='funcionario_apagar'),
]