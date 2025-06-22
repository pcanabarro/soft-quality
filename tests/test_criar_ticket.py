import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page, sync_playwright

from pages.login_page import LoginPage
from pages.portal_home_page import PortalHomePage
from pages.criar_ticket_page import CriarTicketPage

load_dotenv()

@pytest.fixture(scope="function")
def setup_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        browser.close()

def test_criar_novo_ticket(setup_browser: Page):
    page = setup_browser

    usuario = os.getenv("LOGIN_USERNAME")
    senha = os.getenv("LOGIN_PASSWORD")
    login_url = os.getenv("LOGIN_URL")
    home_url = os.getenv("HOME_URL")
    create_ticket_url = os.getenv("CREATE_TICKET_URL")

    assert usuario, "Erro: LOGIN_USERNAME não definido"
    assert senha, "Erro: LOGIN_PASSWORD não definido"
    assert login_url, "Erro: LOGIN_URL não definido"
    assert home_url, "Erro: HOME_URL não definido"
    assert create_ticket_url, "Erro: CREATE_TICKET_URL não definido"

    login_page = LoginPage(page, login_url)
    portal_home_page = PortalHomePage(page, home_url)
    criar_ticket_page = CriarTicketPage(page, create_ticket_url)

    print("\n--- Iniciando teste de Criação de Ticket ---")

    print("Passo 1: Realizando login...")
    login_page.navegar()
    login_page.fazer_login(usuario, senha)
    assert portal_home_page.esta_na_pagina_inicial(), \
        "Login falhou ou redirecionamento incorreto."

    print("Passo 2: Acessando formulário de ticket...")
    criar_ticket_page.navegar_para_formulario()

    print("Passo 3: Selecionando cliente...")
    criar_ticket_page.selecionar_cliente("BRAIN CONSULTING")

    print("Passo 4: Selecionando projeto...")
    criar_ticket_page.selecionar_projeto("BACKOFFICE")

    print("Passo 5: Selecionando tipo de solicitação...")
    criar_ticket_page.selecionar_solicitacao("34")

    print("Passo 6: Preenchendo descrição...")
    descricao = "THIS IS AN AUTOMATED TEST USING PLAYWRIGHT"
    criar_ticket_page.preencher_descricao(descricao)

    print("Passo 7: Preenchendo produto SAP...")
    criar_ticket_page.preencher_produto_sap("S4 HANA")

    print("Passo 8: Selecionando Role SAP...")
    criar_ticket_page.selecionar_role_sap("186")

    print("Passo 9: Clicando para abrir ticket...")
    criar_ticket_page.clicar_abrir_ticket()

    print("Passo 10: Validando redirecionamento...")
    try:
        page.wait_for_load_state("networkidle", timeout=30000)
        print("✅ Ticket criado com sucesso.")
    except Exception as e:
        print(f"❌ Erro após tentar criar o ticket: {e}")
        page.screenshot(path="ticket_falhou.png")
        raise
