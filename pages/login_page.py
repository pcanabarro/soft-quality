# pages/login_page.py
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page, login_url: str):
        self.page = page
        self.login_url = login_url
        # Seletores
        self.username_input = page.locator("#login")
        self.password_input = page.locator("#password_sem_md5")
        self.login_button = page.locator("button:has-text('Entrar')")

    def navegar(self):
        """Navega para a página de login usando a URL fornecida."""
        print(f"Navegando para a URL de login: {self.login_url}")
        self.page.goto(self.login_url)

    def fazer_login(self, username, password):
        """
        Preenche os campos de login e clica no botão Entrar.
        """
        print(f"Preenchendo o usuário: {username}")
        self.username_input.fill(username)

        print("Preenchendo a senha...")
        self.password_input.fill(password)

        print("Clicando no botão 'Entrar'...")
        self.login_button.click()