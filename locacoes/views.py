from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Locacao, Multa
from .forms import LocacaoModelForm, MultaModelForm, LocacaoFilmeFormSet


# ==================== LOCAÇÕES ====================

class LocacaoListView(ListView):
    model = Locacao
    template_name = 'locacoes.html'
    context_object_name = 'locacoes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('cliente', 'funcionario')
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(cliente__nome__icontains=buscar)
        return qs


class LocacaoCreateView(SuccessMessageMixin, CreateView):
    model = Locacao
    form_class = LocacaoModelForm
    template_name = 'locacao_form.html'
    success_url = reverse_lazy('locacoes')
    success_message = 'Locação cadastrada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LocacaoFilmeFormSet(self.request.POST)
        else:
            context['formset'] = LocacaoFilmeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.valor = Decimal('0.00')
            self.object.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()


                total = Decimal('0.00')
                for item in self.object.locacaofilme_set.all():
                    total += item.filme.valor * item.quantidade

                    filme = item.filme
                    filme.estoque -= item.quantidade
                    if filme.estoque <= 0:
                        filme.disponivel = False
                    filme.save()

                self.object.valor = total
                self.object.save()


                self.enviar_email_locacao(self.object)

                return super().form_valid(form)
            else:
                return self.form_invalid(form)

    def enviar_email_locacao(self, locacao):
        try:
            cliente = locacao.cliente
            assunto = f'Confirmação de Locação #{locacao.id} - Locadora de Filmes'

            contexto = {
                'cliente': cliente,
                'locacao': locacao,
            }

            mensagem_texto = render_to_string('emails/locacao_email.txt', contexto)
            mensagem_html = render_to_string('emails/locacao_email.html', contexto)

            send_mail(
                subject=assunto,
                message=mensagem_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cliente.email],
                html_message=mensagem_html,
                fail_silently=True,
            )
        except Exception as e:
            messages.warning(self.request, f'Locação salva, mas o e-mail não pôde ser enviado: {e}')


class LocacaoUpdateView(SuccessMessageMixin, UpdateView):
    model = Locacao
    form_class = LocacaoModelForm
    template_name = 'locacao_form.html'
    success_url = reverse_lazy('locacoes')
    success_message = 'Locação atualizada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LocacaoFilmeFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = LocacaoFilmeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()


                total = Decimal('0.00')
                for item in self.object.locacaofilme_set.all():
                    total += item.filme.valor * item.quantidade

                self.object.valor = total
                self.object.save()

                return super().form_valid(form)
            else:
                return self.form_invalid(form)


class LocacaoDeleteView(SuccessMessageMixin, DeleteView):
    model = Locacao
    template_name = 'locacao_delete.html'
    success_url = reverse_lazy('locacoes')
    success_message = 'Locação excluída com sucesso!'


class LocacaoDetailView(DetailView):
    model = Locacao
    template_name = 'locacao_detalhe.html'
    context_object_name = 'locacao'


# ==================== MULTAS ====================

class MultaListView(ListView):
    model = Multa
    template_name = 'multas.html'
    context_object_name = 'multas'
    paginate_by = 10


class MultaCreateView(SuccessMessageMixin, CreateView):
    model = Multa
    form_class = MultaModelForm
    template_name = 'multa_form.html'
    success_url = reverse_lazy('multas')
    success_message = 'Multa cadastrada com sucesso!'


class MultaUpdateView(SuccessMessageMixin, UpdateView):
    model = Multa
    form_class = MultaModelForm
    template_name = 'multa_form.html'
    success_url = reverse_lazy('multas')
    success_message = 'Multa atualizada com sucesso!'


class MultaDeleteView(SuccessMessageMixin, DeleteView):
    model = Multa
    template_name = 'multa_delete.html'
    success_url = reverse_lazy('multas')
    success_message = 'Multa excluída com sucesso!'

class LocacaoDevolverView(View):
    def post(self, request, pk):
        locacao = get_object_or_404(Locacao, pk=pk)

        if locacao.status != 'A':
            messages.error(request, 'Esta locação já foi finalizada ou cancelada.')
            return redirect('locacao_detalhe', pk=pk)

        try:
            multa_valor, dias = locacao.devolver(valor_multa_por_dia=Decimal('5.00'))

            if multa_valor > 0:
                messages.warning(
                    request,
                    f'Locação devolvida com atraso de {dias} dia(s). Multa gerada: R$ {multa_valor}'
                )
            else:
                messages.success(request, 'Locação devolvida com sucesso! Sem multa.')

        except Exception as e:
            messages.error(request, f'Erro ao devolver: {e}')

        return redirect('locacao_detalhe', pk=pk)