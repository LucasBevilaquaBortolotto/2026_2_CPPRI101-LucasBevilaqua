from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Q

from locacoes.models import Multa, Locacao
from .models import Caixa, Transacao, CompraVendaFilme
from .forms import CaixaModelForm, TransacaoModelForm, CompraVendaFilmeModelForm


# ==================== CAIXA ====================

class CaixaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'caixa.view_caixa'
    model = Caixa
    template_name = 'caixas.html'
    context_object_name = 'caixas'
    paginate_by = 10


class CaixaCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'caixa.add_caixa'
    model = Caixa
    form_class = CaixaModelForm
    template_name = 'caixa_form.html'
    success_url = reverse_lazy('caixas')
    success_message = 'Caixa aberto com sucesso!'


class CaixaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'caixa.change_caixa'
    model = Caixa
    form_class = CaixaModelForm
    template_name = 'caixa_form.html'
    success_url = reverse_lazy('caixas')
    success_message = 'Caixa atualizado com sucesso"'


class CaixaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'caixa.delete_caixa'
    model = Caixa
    template_name = 'caixa_delete.html'
    success_url = reverse_lazy('caixas')
    success_message = 'Caixa excluído com sucesso!'


class CaixaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'caixa.view_caixa'
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

class CaixaFecharView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'caixa.change_caixa'
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

class TransacaoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Transacao
    template_name = 'transacoes.html'
    context_object_name = 'transacoes'
    paginate_by = 15
    permission_required = 'caixa.view_transacao'

    def get_queryset(self):
        return super().get_queryset().select_related('caixa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Só locações finalizadas que AINDA NÃO foram registradas no caixa
        total_locacoes = Locacao.objects.filter(
            status='F',
            registrado_caixa=False
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

        # Só multas pendentes
        total_multas = Multa.objects.filter(
            status='P'
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

        total_geral = total_locacoes + total_multas

        caixa_aberto = Caixa.objects.filter(data_fechar__isnull=True).first()

        context['total_locacoes'] = total_locacoes
        context['total_multas'] = total_multas
        context['total_geral'] = total_geral
        context['caixa_aberto'] = caixa_aberto

        return context


class TransacaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'caixa.add_transacao'
    model = Transacao
    form_class = TransacaoModelForm
    template_name = 'transacao_form.html'
    success_url = reverse_lazy('transacoes')
    success_message = 'Transação registrada com sucesso!'


class TransacaoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'caixa.change_transacao'
    model = Transacao
    form_class = TransacaoModelForm
    template_name = 'transacao_form.html'
    success_url = reverse_lazy('transacoes')
    success_message = 'Transação atualizada com sucesso!'


class TransacaoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'caixa.delete_transacao'
    model = Transacao
    template_name = 'transacao_delete.html'
    success_url = reverse_lazy('transacoes')
    success_message = 'Transação excluída com sucesso!'


# ==================== COMPRA / VENDA ====================

class CompraVendaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'caixa.view_compravendafilme'
    model = CompraVendaFilme
    template_name = 'compras_vendas.html'
    context_object_name = 'compras_vendas'
    paginate_by = 15


class CompraVendaCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'caixa.add_compravendafilme'
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


class CompraVendaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'caixa.change_compravendafilme'
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


class CompraVendaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'caixa.delete_compravendafilme'
    model = CompraVendaFilme
    template_name = 'compra_venda_delete.html'
    success_url = reverse_lazy('compras_vendas')
    success_message = 'Registro excluído com sucesso!'

    def form_valid(self, form):
        with transaction.atomic():

            self.object.atualizar_estoque(reverter=True)
            return super().form_valid(form)

class GerarTransacaoLocacoesMultasView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'caixa.add_transacao'

    def post(self, request):
        caixa_aberto = Caixa.objects.filter(data_fechar__isnull=True).first()

        if not caixa_aberto:
            messages.error(request, 'Não existe nenhum caixa aberto. Abra um caixa antes de registrar a transação.')
            return redirect('transacoes')

        # Locações ainda não registradas
        locacoes = Locacao.objects.filter(status='F', registrado_caixa=False)
        total_locacoes = locacoes.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

        # Multas pendentes
        multas = Multa.objects.filter(status='P')
        total_multas = multas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

        total_geral = total_locacoes + total_multas

        if total_geral <= 0:
            messages.warning(request, 'Não há valores de locações ou multas para registrar.')
            return redirect('transacoes')

        # Cria a transação
        Transacao.objects.create(
            caixa=caixa_aberto,
            valor=total_geral,
            data=timezone.now().date(),
            descricao=f'Recebimento de Locações (R$ {total_locacoes}) + Multas (R$ {total_multas})',
            tipo='E'
        )

        # Marca as locações como já registradas no caixa
        locacoes.update(registrado_caixa=True)

        # Marca as multas como pagas
        multas.update(status='Q', data_pagamento=timezone.now().date())

        messages.success(request, f'Transação criada com sucesso! Valor total: R$ {total_geral}')
        return redirect('transacoes')