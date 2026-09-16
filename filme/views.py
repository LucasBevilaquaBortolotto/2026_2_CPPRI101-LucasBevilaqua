from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from .forms import FilmeForm
from .models import Filme


class FilmeView(ListView):
    model = Filme
    template_name = 'catalogo.html'
    context_object_name = 'filme'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        return qs

class FilmeAddView(CreateView):
    model = Filme
    form_class = FilmeForm
    template_name = 'filme_forms.html'
    success_url = reverse_lazy('filme')