"""Testes funcionais do LocalEats com Playwright (Parte 2)."""

import re
from pathlib import Path

from playwright.sync_api import Page, expect

from pages.home_page import HomePage

EVIDENCIAS = Path(__file__).resolve().parent.parent / "evidencias"
CLASSE_ATIVA = re.compile(r"\bactive\b")


# Responsável: Thiago Figueiredo
def test_filtrar_categoria_brasileira_exibe_somente_restaurantes_brasileiros(
    usuario_autenticado: Page,
):
    # Arrange
    home = HomePage(usuario_autenticado)
    home.aguardar_restaurantes()

    # Act
    home.filtrar_por_categoria("Brasileira")

    # Assert
    expect(home.botao_categoria("Brasileira")).to_have_class(CLASSE_ATIVA)
    expect(home.cards_restaurantes).to_have_count(2)
    expect(home.cards_restaurantes).to_contain_text(["Brasileira", "Brasileira"])
    expect(home.cards_restaurantes.filter(has_text="Japonesa")).to_have_count(0)

    usuario_autenticado.screenshot(
        path=EVIDENCIAS / "tf01_categoria_brasileira.png", full_page=True
    )


# Responsável: Gabriel Matiolla
def test_pesquisar_por_localizacao_centro_exibe_restaurantes_do_centro(
    usuario_autenticado: Page,
):
    # Arrange
    home = HomePage(usuario_autenticado)
    home.aguardar_restaurantes()

    # Act
    home.pesquisar("Centro")

    # Assert
    expect(home.cards_restaurantes).to_have_count(4)
    expect(home.cards_restaurantes).to_contain_text(["Centro"] * 4)
    expect(home.cards_restaurantes.filter(has_text="Zona Sul")).to_have_count(0)
    expect(home.campo_busca).to_have_value("Centro")

    usuario_autenticado.screenshot(
        path=EVIDENCIAS / "tf02_pesquisa_centro.png", full_page=True
    )
