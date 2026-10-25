from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Q
from .models import Caixa, Transacao, CompraVendaFilme
from .forms import CaixaModelForm, TransacaoModelForm, CompraVendaFilmeModelForm


# ==================== CAIXA ====================

class CaixaListView(ListView):
    model = Caixa
    template_name = 'caixas.html'
    context_object_name = 'caixas'
    paginate_by = 10


class CaixaCreateView(SuccessMessageMixin, CreateView):
    model = Caixa
    form_class = CaixaModelForm
    template_name = 'caixa_form.html'
    success_url = reverse_lazy('caixas')
    success_message = 'Caixa aberto com sucesso!'


class CaixaUpdateView(SuccessMessageMixin, UpdateView):
    model = Caixa
    form_class = CaixaModelForm
    template_name = 'caixa_form.html'
    success_url = reverse_lazy('caixas')
    success_message = 'Caixa atualizado com sucesso!'


class CaixaDeleteView(SuccessMessageMixin, DeleteView):
    model = Caixa
    template_name = 'caixa_delete.html'
    success_url = reverse_lazy('caixas')
    success_message = 'Caixa excluído com sucesso!'


class CaixaDetailView(DetailView):
    model = Caixa
    template_name = 'caixa_detalhe.html'
    context_object_name = 'caixa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caixa = self.object
        transacoes = caixa.transacoes.all()

        total_entradas = transacoes.filter(tipo='E').aggregate(total=Sum('valor'))['total'] or 0
        total_saidas = transacoes.filter(tipo='S').aggregate(total=Sum('valor'))['total'] or 0

        context['transacoes'] = transacoes
        context['total_entradas'] = total_entradas
        context['total_saidas'] = total_saidas
        context['saldo_atual'] = caixa.saldo_inicial + total_entradas - total_saidas
        return context

class CaixaFecharView(View):
    def post(self, request, pk):
        caixa = get_object_or_404(Caixa, pk=pk)

        if not caixa.esta_aberto:
            messages.error(request, 'Este caixa já está fechado.')
            return redirect('caixa_detalhe', pk=pk)

        try:
            total_entradas, total_saidas, saldo_final = caixa.fechar()

            messages.success(
                request,
                f'Caixa fechado com sucesso! '
                f'Entradas: R$ {total_entradas} | '
                f'Saídas: R$ {total_saidas} | '
                f'Saldo Final: R$ {saldo_final}'
            )
        except Exception as e:
            messages.error(request, f'Erro ao fechar o caixa: {e}')

        return redirect('caixa_detalhe', pk=pk)


# ==================== TRANSAÇÕES ====================

class TransacaoListView(ListView):
    model = Transacao
    template_name = 'transacoes.html'
    context_object_name = 'transacoes'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().select_related('caixa')


class TransacaoCreateView(SuccessMessageMixin, CreateView):
    model = Transacao
    form_class = TransacaoModelForm
    template_name = 'transacao_form.html'
    success_url = reverse_lazy('transacoes')
    success_message = 'Transação registrada com sucesso!'


class TransacaoUpdateView(SuccessMessageMixin, UpdateView):
    model = Transacao
    form_class = TransacaoModelForm
    template_name = 'transacao_form.html'
    success_url = reverse_lazy('transacoes')
    success_message = 'Transação atualizada com sucesso!'


class TransacaoDeleteView(SuccessMessageMixin, DeleteView):
    model = Transacao
    template_name = 'transacao_delete.html'
    success_url = reverse_lazy('transacoes')
    success_message = 'Transação excluída com sucesso!'


# ==================== COMPRA / VENDA ====================

class CompraVendaListView(ListView):
    model = CompraVendaFilme
    template_name = 'compras_vendas.html'
    context_object_name = 'compras_vendas'
    paginate_by = 15


class CompraVendaCreateView(SuccessMessageMixin, CreateView):
    model = CompraVendaFilme
    form_class = CompraVendaFilmeModelForm
    template_name = 'compra_venda_form.html'
    success_url = reverse_lazy('compras_vendas')
    success_message = 'Registro de compra/venda criado com sucesso!'

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()

            self.object.atualizar_estoque()
        return super().form_valid(form)


class CompraVendaUpdateView(SuccessMessageMixin, UpdateView):
    model = CompraVendaFilme
    form_class = CompraVendaFilmeModelForm
    template_name = 'compra_venda_form.html'
    success_url = reverse_lazy('compras_vendas')
    success_message = 'Registro atualizado com sucesso!'

    def form_valid(self, form):
        with transaction.atomic():

            old_obj = CompraVendaFilme.objects.get(pk=self.object.pk)
            old_obj.atualizar_estoque(reverter=True)


            self.object = form.save()


            self.object.atualizar_estoque()
        return super().form_valid(form)


class CompraVendaDeleteView(SuccessMessageMixin, DeleteView):
    model = CompraVendaFilme
    template_name = 'compra_venda_delete.html'
    success_url = reverse_lazy('compras_vendas')
    success_message = 'Registro excluído com sucesso!'

    def form_valid(self, form):
        with transaction.atomic():

            self.object.atualizar_estoque(reverter=True)
            return super().form_valid(form)