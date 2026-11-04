from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Cliente, Funcionario
from .forms import ClienteModelForm, FuncionarioModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# ==================== CLIENTES ====================

class ClienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'pessoas.view_cliente'
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


class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'pessoas.add_cliente'
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso!'


class ClienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'pessoas.change_cliente'
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso!'


class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'pessoas.delete_cliente'
    model = Cliente
    template_name = 'cliente_delete.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente excluído com sucesso!'


# ==================== FUNCIONÁRIOS ====================

class FuncionarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'pessoas.view_funcionario'
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


class FuncionarioCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'pessoas.add_funcionario'
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário cadastrado com sucesso!'


class FuncionarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'pessoas.change_funcionario'
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário atualizado com sucesso!'


class FuncionarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'pessoas.delete_funcionario'
    model = Funcionario
    template_name = 'funcionario_delete.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário excluído com sucesso!'
