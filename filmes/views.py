from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Filme
from .forms import FilmeModelForm


class FilmeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'filmes.view_filme'
    model = Filme
    template_name = 'filmes.html'
    context_object_name = 'filmes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(titulo__icontains=buscar)
        return qs


class FilmeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'filmes.add_filme'
    model = Filme
    form_class = FilmeModelForm
    template_name = 'filme_form.html'
    success_url = reverse_lazy('filmes')
    success_message = 'Filme cadastrado com sucesso!'


class FilmeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'filmes.change_filme'
    model = Filme
    form_class = FilmeModelForm
    template_name = 'filme_form.html'
    success_url = reverse_lazy('filmes')
    success_message = 'Filme atualizado com sucesso!'


class FilmeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'filmes.delete_filme'
    model = Filme
    template_name = 'filme_delete.html'
    success_url = reverse_lazy('filmes')
    success_message = 'Filme excluído com sucesso!'