from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Filme
from .forms import FilmeModelForm


class FilmeListView(ListView):
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


class FilmeCreateView(SuccessMessageMixin, CreateView):
    model = Filme
    form_class = FilmeModelForm
    template_name = 'filme_form.html'
    success_url = reverse_lazy('filmes')
    success_message = 'Filme cadastrado com sucesso!'


class FilmeUpdateView(SuccessMessageMixin, UpdateView):
    model = Filme
    form_class = FilmeModelForm
    template_name = 'filme_form.html'
    success_url = reverse_lazy('filmes')
    success_message = 'Filme atualizado com sucesso!'


class FilmeDeleteView(SuccessMessageMixin, DeleteView):
    model = Filme
    template_name = 'filme_delete.html'
    success_url = reverse_lazy('filmes')
    success_message = 'Filme excluído com sucesso!'