"""Page Object da página de detalhes de um restaurante do LocalEats."""

from playwright.sync_api import Page


class RestaurantePage:
    def __init__(self, page: Page):
        self.page = page
        self.nome = page.get_by_role("heading", level=2)
        self.aba_cardapio = page.get_by_role("button", name="Cardápio")
        self.aba_avaliacoes = page.get_by_role("button", name="Avaliações")
        self.carrinho = page.locator("#floatingCart")
        self.contador_carrinho = page.locator("#cartCountBadge")
        self.itens_carrinho = page.locator("#cartItemsList")

    def aba(self, nome_aba):
        return self.page.get_by_role("button", name=nome_aba)

    def selecionar_aba(self, nome_aba):
        self.aba(nome_aba).click()

    def avaliacao(self, comentario):
        return self.page.get_by_text(comentario)

    def adicionar_ao_carrinho(self, nome_prato):
        self.page.locator(".menu-item").filter(has_text=nome_prato).get_by_role(
            "button", name="Adicionar"
        ).click()
