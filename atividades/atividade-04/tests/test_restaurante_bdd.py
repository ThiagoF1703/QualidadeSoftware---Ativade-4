"""Automação BDD (pytest-bdd + Playwright) dos cenários de restaurante."""

import re

from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenario, then, when

from pages.home_page import HomePage
from pages.restaurante_page import RestaurantePage

FEATURE = "../features/restaurante.feature"
CLASSE_ATIVA = re.compile(r"\bactive\b")


# Responsável: Thiago Figueiredo
@scenario(FEATURE, "Consultar as avaliações de um restaurante")
def test_consultar_avaliacoes_de_um_restaurante():
    pass


# Responsável: Gabriel Matiolla
@scenario(FEATURE, "Adicionar um prato ao carrinho")
def test_adicionar_prato_ao_carrinho():
    pass


# ----------------------------- Dado ---------------------------------------

@given("que estou autenticado no LocalEats")
def estou_autenticado(usuario_autenticado: Page):
    HomePage(usuario_autenticado).aguardar_restaurantes()


@given(parsers.parse('que abri os detalhes do restaurante "{nome}"'))
def abrir_detalhes(page: Page, nome):
    HomePage(page).abrir_restaurante(nome)
    expect(RestaurantePage(page).nome).to_have_text(nome)


# ----------------------------- Quando -------------------------------------

@when(parsers.parse('seleciono a aba "{aba}"'))
def selecionar_aba(page: Page, aba):
    RestaurantePage(page).selecionar_aba(aba)


@when(parsers.parse('adiciono o prato "{prato}" ao carrinho'))
def adicionar_prato(page: Page, prato):
    RestaurantePage(page).adicionar_ao_carrinho(prato)


# ----------------------------- Então --------------------------------------

@then(parsers.parse('a aba "{aba}" deve estar selecionada'))
def aba_selecionada(page: Page, aba):
    restaurante = RestaurantePage(page)
    expect(restaurante.aba(aba)).to_have_class(CLASSE_ATIVA)
    expect(restaurante.aba_cardapio).not_to_have_class(CLASSE_ATIVA)


@then(parsers.parse('a avaliação "{comentario}" deve ser apresentada'))
def avaliacao_apresentada(page: Page, comentario):
    expect(RestaurantePage(page).avaliacao(comentario)).to_be_visible()


@then(parsers.parse('o carrinho deve indicar "{quantidade}"'))
def carrinho_indica(page: Page, quantidade):
    restaurante = RestaurantePage(page)
    expect(restaurante.carrinho).to_have_class(CLASSE_ATIVA)
    expect(restaurante.contador_carrinho).to_have_text(quantidade)


@then(parsers.parse('o carrinho deve listar "{item}"'))
def carrinho_lista(page: Page, item):
    expect(RestaurantePage(page).itens_carrinho).to_contain_text(item)
