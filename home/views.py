from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q
from decimal import Decimal

from pessoas.models import Cliente, Funcionario
from filmes.models import Filme
from locacoes.models import Locacao, Multa
from caixa.models import Caixa, Transacao


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ===== PESSOAS =====
        context['total_clientes'] = Cliente.objects.count()
        context['clientes_ativos'] = Cliente.objects.filter(ativo=True).count()
        context['total_funcionarios'] = Funcionario.objects.count()

        # ===== FILMES =====
        context['total_filmes'] = Filme.objects.count()
        context['filmes_disponiveis'] = Filme.objects.filter(disponivel=True).count()
        context['filmes_indisponiveis'] = Filme.objects.filter(disponivel=False).count()
        context['estoque_total'] = Filme.objects.aggregate(total=Sum('estoque'))['total'] or 0

        # ===== LOCAÇÕES =====
        context['total_locacoes'] = Locacao.objects.count()
        context['locacoes_abertas'] = Locacao.objects.filter(status='A').count()
        context['locacoes_finalizadas'] = Locacao.objects.filter(status='F').count()
        context['locacoes_atrasadas'] = Locacao.objects.filter(status='A').count()  # vamos filtrar melhor abaixo

        # Locações atrasadas de verdade
        from django.utils import timezone
        hoje = timezone.now().date()
        context['locacoes_atrasadas'] = Locacao.objects.filter(
            status='A',
            data_devolucao__lt=hoje
        ).count()

        # ===== MULTAS =====
        context['total_multas'] = Multa.objects.count()
        context['multas_pendentes'] = Multa.objects.filter(status='P').count()
        context['valor_multas_pendentes'] = Multa.objects.filter(status='P').aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0.00')

        # ===== CAIXA =====
        caixa_aberto = Caixa.objects.filter(data_fechar__isnull=True).first()
        context['caixa_aberto'] = caixa_aberto

        if caixa_aberto:
            total_entradas, total_saidas, saldo_atual = caixa_aberto.calcular_totais()
            context['saldo_caixa_atual'] = saldo_atual
            context['entradas_caixa'] = total_entradas
            context['saidas_caixa'] = total_saidas
        else:
            context['saldo_caixa_atual'] = Decimal('0.00')
            context['entradas_caixa'] = Decimal('0.00')
            context['saidas_caixa'] = Decimal('0.00')

        # Últimas locações
        context['ultimas_locacoes'] = Locacao.objects.select_related(
            'cliente', 'funcionario'
        ).order_by('-data_locacao')[:5]

        # Filmes com estoque baixo (≤ 2)
        context['filmes_estoque_baixo'] = Filme.objects.filter(estoque__lte=2).order_by('estoque')[:5]

        return context