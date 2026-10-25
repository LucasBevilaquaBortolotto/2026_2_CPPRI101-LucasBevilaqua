from django.urls import path
from .views import FilmeListView, FilmeCreateView, FilmeUpdateView, FilmeDeleteView

urlpatterns = [
    path('filmes/', FilmeListView.as_view(), name='filmes'),
    path('filmes/novo/', FilmeCreateView.as_view(), name='filme_novo'),
    path('filmes/editar/<int:pk>/', FilmeUpdateView.as_view(), name='filme_editar'),
    path('filmes/excluir/<int:pk>/', FilmeDeleteView.as_view(), name='filme_excluir'),
]