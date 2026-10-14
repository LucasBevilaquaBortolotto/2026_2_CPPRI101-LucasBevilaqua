from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from .models import Filme, Locacao, Cliente, Funcionario
from .forms import LocacaoModelForm, ClienteModelForm, FuncionarioModelForm, LocacaoUpdateModelForm
from django.views.generic import TemplateView

class FilmesView(ListView):
    model = Filme
    template_name = 'filmes.html'
    context_object_name = 'filmes'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(titulo__icontains=buscar) | Q(genero__icontains=buscar)
            )
        return queryset


class FilmeAddView(SuccessMessageMixin, CreateView):
    model = Filme
    template_name = 'filme_form.html'
    fields = ['titulo', 'genero', 'anoLancamento', 'classEtaria', 'valor', 'estoque', 'disponivel']
    success_url = reverse_lazy('filmes')
    success_message = "Filme cadastrado com sucesso!"


class FilmeUpdateView(SuccessMessageMixin, UpdateView):
    model = Filme
    template_name = 'filme_form.html'
    fields = ['titulo', 'genero', 'anoLancamento', 'classEtaria', 'valor', 'estoque', 'disponivel']
    success_url = reverse_lazy('filmes')
    success_message = "Filme atualizado com sucesso!"


class FilmeDeleteView(SuccessMessageMixin, DeleteView):
    model = Filme
    template_name = 'filme_delete.html'
    success_url = reverse_lazy('filmes')
    success_message = "Filme excluído com sucesso!"


class LocacoesView(ListView):
    model = Locacao
    template_name = 'locacoes.html'
    context_object_name = 'locacoes'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(cliente__nome__icontains=buscar) | Q(status__icontains=buscar)
            )
        return queryset


class LocacaoAddView(SuccessMessageMixin, CreateView):
    model = Locacao
    form_class = LocacaoModelForm
    template_name = 'locacao_form.html'
    success_url = reverse_lazy('locacoes')
    success_message = "Locação realizada com sucesso!"



class HomeView(TemplateView):
    template_name = 'home.html'

class ClientesView(ListView):
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'clientes'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(nome__icontains=buscar) | Q(email__icontains=buscar)
            )
        return queryset


class ClienteAddView(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = "Cliente cadastrado com sucesso!"

class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = "Cliente atualizado com sucesso!"

class FuncionariosView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'
    context_object_name = 'funcionarios'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(nome__icontains=buscar) | Q(cargo__icontains=buscar) | Q(email__icontains=buscar)
            )
        return queryset


class FuncionarioAddView(SuccessMessageMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionarios_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = "Funcionário cadastrado com sucesso!"


class FuncionarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionarios_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = "Funcionário atualizado com sucesso!"


class FuncionarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario_delete.html'
    success_url = reverse_lazy('funcionarios')
    success_message = "Funcionário excluído com sucesso!"

class LocacaoUpdateView(SuccessMessageMixin, UpdateView):
    model = Locacao
    form_class = LocacaoUpdateModelForm
    template_name = 'locacao_form.html'  # Reutiliza o formulário de cadastro
    success_url = reverse_lazy('locacoes')
    success_message = "Locação atualizada com sucesso!"