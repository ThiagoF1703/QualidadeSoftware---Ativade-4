"""Page Object da página inicial (Explorar) do LocalEats."""

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.campo_busca = page.get_by_placeholder(
            "Buscar por culinária ou localização..."
        )
        self.botao_buscar = page.get_by_role("button", name="Buscar", exact=True)
        # Cada restaurante é exibido como um link (card) dentro da grade
        self.cards_restaurantes = page.locator("#restaurantGrid").get_by_role("link")

    def aguardar_restaurantes(self):
        """Espera a carga inicial da grade, sem pausas fixas."""
        expect(self.cards_restaurantes.first).to_be_visible()

    def botao_categoria(self, categoria):
        return self.page.get_by_role("button", name=categoria, exact=True)

    def filtrar_por_categoria(self, categoria):
        self.botao_categoria(categoria).click()

    def pesquisar(self, texto):
        self.campo_busca.fill(texto)
        self.botao_buscar.click()

    def abrir_restaurante(self, nome):
        self.cards_restaurantes.filter(has_text=nome).click()
