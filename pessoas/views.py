from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Cliente, Funcionario
from .forms import ClienteModelForm, FuncionarioModelForm


# ==================== CLIENTES ====================

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        return qs


class ClienteCreateView(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso!'


class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso!'


class ClienteDeleteView(SuccessMessageMixin, DeleteView):
    model = Cliente
    template_name = 'cliente_delete.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente excluído com sucesso!'


# ==================== FUNCIONÁRIOS ====================

class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'
    context_object_name = 'funcionarios'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        return qs


class FuncionarioCreateView(SuccessMessageMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário cadastrado com sucesso!'


class FuncionarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário atualizado com sucesso!'


class FuncionarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario_delete.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário excluído com sucesso!'
