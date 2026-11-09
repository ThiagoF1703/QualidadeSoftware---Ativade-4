"""Testes unitários das regras de negócio do LocalEats (Parte 1 - TDD)."""

import pytest

from src.regras_localeats import calcular_desconto, pedido_atingiu_valor_minimo


# ---------------------------------------------------------------------------
# Regra 1: valor mínimo do pedido
# Responsável: Thiago Figueiredo
# ---------------------------------------------------------------------------

# Responsável: Thiago Figueiredo
def test_pedido_acima_do_minimo_retorna_true():
    resultado = pedido_atingiu_valor_minimo(50)
    assert resultado is True


# Responsável: Thiago Figueiredo
def test_pedido_abaixo_do_minimo_retorna_false():
    resultado = pedido_atingiu_valor_minimo(29.99)
    assert resultado is False


# Responsável: Thiago Figueiredo
def test_pedido_exatamente_no_valor_minimo_retorna_true():
    resultado = pedido_atingiu_valor_minimo(30)
    assert resultado is True


# Responsável: Thiago Figueiredo
def test_valor_minimo_rejeita_valor_negativo():
    with pytest.raises(ValueError):
        pedido_atingiu_valor_minimo(-1)


# ---------------------------------------------------------------------------
# Regra 2: desconto do pedido
# Responsável: Gabriel Matiolla
# ---------------------------------------------------------------------------

# Responsável: Gabriel Matiolla
def test_pedido_abaixo_de_cem_nao_recebe_desconto():
    desconto = calcular_desconto(80)
    assert desconto == 0


# Responsável: Gabriel Matiolla
def test_pedido_de_cem_ou_mais_recebe_dez_porcento_de_desconto():
    desconto = calcular_desconto(150)
    assert desconto == 15


# Responsável: Gabriel Matiolla
@pytest.mark.parametrize(
    ("valor_pedido", "desconto_esperado"),
    [
        (99.99, 0),     # imediatamente abaixo do limite
        (100, 10),      # exatamente no limite
        (101, 10.10),   # caso que expôs o erro de ponto flutuante
    ],
)
def test_desconto_nos_limites_da_regra(valor_pedido, desconto_esperado):
    assert calcular_desconto(valor_pedido) == desconto_esperado


# Responsável: Gabriel Matiolla
def test_desconto_rejeita_valor_negativo():
    with pytest.raises(ValueError):
        calcular_desconto(-10)
