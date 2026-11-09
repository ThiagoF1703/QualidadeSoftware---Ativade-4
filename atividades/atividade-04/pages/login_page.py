"""Page Object da tela de login/cadastro do LocalEats."""

from playwright.sync_api import Page


class LoginPage:
    URL = "https://local-eats-unisenac.vercel.app/static/login.html"

    def __init__(self, page: Page):
        self.page = page
        self.aba_criar_conta = page.get_by_role("button", name="Criar Conta")
        self.campo_nome = page.get_by_placeholder("Seu nome")
        self.campo_email = page.get_by_placeholder("novo@teste.com")
        self.campo_senha = page.get_by_placeholder("Min. 3 caracteres")
        self.botao_registrar = page.get_by_role("button", name="Registrar")

    def abrir(self):
        self.page.goto(self.URL)

    def criar_conta(self, nome, email, senha):
        self.aba_criar_conta.click()
        self.campo_nome.fill(nome)
        self.campo_email.fill(email)
        self.campo_senha.fill(senha)
        self.botao_registrar.click()
