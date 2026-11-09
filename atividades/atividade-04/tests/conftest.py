"""Fixtures compartilhadas pelos testes funcionais e BDD."""

import re
import uuid

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

# Dados de teste: cada teste cria uma conta nova e descartável,
# o que mantém os testes independentes entre si (sem dados compartilhados).
NOME_TESTE = "Dupla Teste LocalEats"
SENHA_TESTE = "teste123"


@pytest.fixture
def usuario_autenticado(page: Page):
    """Cria uma conta de teste pela interface e chega à página inicial."""
    email = f"dupla.{uuid.uuid4().hex[:10]}@teste.com"
    login = LoginPage(page)
    login.abrir()
    login.criar_conta(NOME_TESTE, email, SENHA_TESTE)
    expect(page).to_have_url(re.compile(r"/static/index\.html$"))
    return page
