"""Regras de negócio do LocalEats - Atividade 4.

Regra 1 (Thiago Figueiredo): pedido_atingiu_valor_minimo
Regra 2 (Gabriel Matiolla): calcular_desconto
"""

VALOR_MINIMO_PEDIDO = 30
VALOR_MINIMO_PARA_DESCONTO = 100
PERCENTUAL_DESCONTO = 10


def _validar_valor_pedido(valor_pedido):
    """Rejeita valores negativos, regra comum às duas funções."""
    if valor_pedido < 0:
        raise ValueError("O valor do pedido não pode ser negativo.")


# Responsável: Thiago Figueiredo
def pedido_atingiu_valor_minimo(valor_pedido):
    """Retorna True quando o pedido atinge o valor mínimo de R$ 30,00."""
    _validar_valor_pedido(valor_pedido)
    return valor_pedido >= VALOR_MINIMO_PEDIDO


# Responsável: Gabriel Matiolla
def calcular_desconto(valor_pedido):
    """Retorna o valor do desconto (não o valor final do pedido).

    Pedidos de R$ 100,00 ou mais recebem 10% de desconto.
    O resultado é arredondado em 2 casas por representar dinheiro.
    """
    _validar_valor_pedido(valor_pedido)
    if valor_pedido < VALOR_MINIMO_PARA_DESCONTO:
        return 0
    return round(valor_pedido * PERCENTUAL_DESCONTO / 100, 2)
