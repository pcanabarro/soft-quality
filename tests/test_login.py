import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page, sync_playwright

# Importa as classes Page Object
from pages.login_page import LoginPage
from pages.portal_home_page import PortalHomePage

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Fixture para configurar o navegador para cada teste
@pytest.fixture(scope="function")
def setup_browser():
    # 'headless=False' para ver a execução no navegador. Mude para 'True' para rodar em background.
    # 'slow_mo=500' adiciona um atraso de 500ms entre as operações. Remova ou ajuste para testes mais rápidos.
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        browser.close()

# Teste de login bem-sucedido
def test_login_sucesso(setup_browser: Page):
    page = setup_browser

    # Obtém credenciais e URLs das variáveis de ambiente
    usuario = os.getenv("LOGIN_USERNAME")
    senha = os.getenv("LOGIN_PASSWORD")
    login_url = os.getenv("LOGIN_URL")
    home_url = os.getenv("HOME_URL")

    # Verifica se todas as variáveis necessárias foram carregadas
    assert usuario, "Erro: Variável de ambiente LOGIN_USERNAME não definida!"
    assert senha, "Erro: Variável de ambiente LOGIN_PASSWORD não definida!"
    assert login_url, "Erro: Variável de ambiente LOGIN_URL não definida!"
    assert home_url, "Erro: Variável de ambiente HOME_URL não definida!"

    # Instancia as Page Objects, passando as URLs e a instância da página do navegador
    login_page = LoginPage(page, login_url)
    portal_home_page = PortalHomePage(page, home_url)

    # --- Fluxo de login ---
    print("Iniciando teste de login...")
    login_page.navegar()
    login_page.fazer_login(usuario, senha)

    # --- Validação do login ---
    try:
        assert portal_home_page.esta_na_pagina_inicial(), "Falha na validação: Redirecionamento para a página inicial do portal não ocorreu como esperado."
        print("Redirecionamento para a URL esperada foi bem-sucedido!")
        print("Teste de login concluído e bem-sucedido! 🎉")
    except AssertionError as e:
        print(f"Teste de login FALHOU! ❌ {e}")
        # Captura de tela para depuração em caso de falha na asserção
        screenshot_path = "login_falhou_url_nao_atingida.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot '{screenshot_path}' salvo para depuração.")
        raise # Re-levanta a exceção para que pytest marque o teste como falho