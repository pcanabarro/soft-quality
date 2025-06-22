from playwright.sync_api import Page, expect

class PortalHomePage:
    def __init__(self, page: Page, expected_url: str):
        self.page = page
        self.expected_url = expected_url
        # Você pode adicionar seletores aqui para elementos específicos da página home do portal
        self.user_profile_link = page.locator("a[id='user-dropdown']") # Exemplo de seletor na página home

    def esta_na_pagina_inicial(self):
        """Verifica se a URL atual corresponde à URL esperada da página inicial do portal."""
        print(f"Verificando se a URL atual é: {self.expected_url}")
        try:
            # wait_for_url para robustez, esperando a URL específica
            self.page.wait_for_url(self.expected_url, timeout=10000) # Timeout em milissegundos
            return True
        except Exception as e:
            print(f"URL esperada '{self.expected_url}' não atingida dentro do tempo limite. Erro: {e}")
            return False

    def get_welcome_message(self):
        """Exemplo: retorna o texto de uma mensagem de boas-vindas (se houver um seletor)."""
        # Implementar seletor e lógica aqui se necessário
        return "Mensagem de boas-vindas (implementar seletor)"