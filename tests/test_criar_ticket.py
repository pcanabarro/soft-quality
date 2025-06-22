# tests/test_criar_ticket.py
import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page, sync_playwright

# Importa as classes Page Object
from pages.login_page import LoginPage
from pages.portal_home_page import PortalHomePage
from pages.criar_ticket_page import CriarTicketPage

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Fixture para configurar o navegador para cada teste
@pytest.fixture(scope="function")
def setup_browser():
    with sync_playwright() as p:
        # Configurações do navegador:
        # headless=False: O navegador será visível durante a execução (útil para depuração).
        # slow_mo=500: Adiciona um atraso de 500ms entre as ações do Playwright para facilitar a visualização.
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page # Cede o controle da 'page' para a função de teste
        browser.close() # Garante que o navegador seja fechado após o teste

# Teste para criar um novo ticket no sistema
def test_criar_novo_ticket(setup_browser: Page):
    page = setup_browser

    # --- 1. Obter credenciais e URLs das variáveis de ambiente ---
    # É fundamental que essas variáveis estejam definidas no seu arquivo .env
    usuario = os.getenv("LOGIN_USERNAME")
    senha = os.getenv("LOGIN_PASSWORD")
    login_url = os.getenv("LOGIN_URL")
    home_url = os.getenv("HOME_URL")
    create_ticket_url = os.getenv("CREATE_TICKET_URL")

    # Valida se as variáveis de ambiente foram carregadas corretamente
    assert usuario, "Erro: Variável de ambiente LOGIN_USERNAME não definida! Verifique seu .env"
    assert senha, "Erro: Variável de ambiente LOGIN_PASSWORD não definida! Verifique seu .env"
    assert login_url, "Erro: Variável de ambiente LOGIN_URL não definida! Verifique seu .env"
    assert home_url, "Erro: Variável de ambiente HOME_URL não definida! Verifique seu .env"
    assert create_ticket_url, "Erro: Variável de ambiente CREATE_TICKET_URL não definida! Verifique seu .env"

    # --- 2. Instanciar as Page Objects ---
    # Cada Page Object recebe a instância 'page' do Playwright e as URLs relevantes.
    login_page = LoginPage(page, login_url)
    portal_home_page = PortalHomePage(page, home_url)
    criar_ticket_page = CriarTicketPage(page, create_ticket_url)

    print("\n--- Iniciando teste de Criação de Ticket ---")

    # --- 3. Pré-condição: Realizar o login ---
    # Reutiliza a lógica de login da LoginPage para garantir que o usuário esteja autenticado.
    print("Passo 1: Realizando login no sistema...")
    login_page.navegar()
    login_page.fazer_login(usuario, senha)
    # Valida que o login foi bem-sucedido e redirecionou para a página inicial esperada.
    assert portal_home_page.esta_na_pagina_inicial(), \
        "Falha na pré-condição: Login não foi bem-sucedido ou não redirecionou para a home page."

    # --- 4. Navegar para a página de Abrir Tickets ---
    # Embora haja um link, para o teste ser mais direto e isolado, navegamos direto para a URL.
    print("Passo 2: Navegando para o formulário de criação de ticket...")
    criar_ticket_page.navegar_para_formulario()

    # --- 5. Preencher os detalhes do ticket ---
    print("Passo 3: Preenchendo os campos do ticket...")
    # Seleção de Cliente: 'BRAIN'
    criar_ticket_page.selecionar_cliente("BRAIN")

    # Seleção de Projeto: 'BACKOFFICE'
    criar_ticket_page.selecionar_projeto("BACKOFFICE")

    # Selecionar Solicitação: "Outros" (value="34")
    criar_ticket_page.selecionar_solicitacao("34")

    # Preencher Descrição
    # A descrição pode incluir um timestamp ou algo único para identificar o ticket gerado em testes reais.
    # Ex: f"THIS IS AN AUTOMATED TEST USING PLAYWRIGHT - {datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Para este exemplo, manteremos a string fixa.
    ticket_description = "THIS IS A AUTOMATED TEST USING PLAYWRIGHT"
    criar_ticket_page.preencher_descricao(ticket_description)

    # Preencher Produto SAP
    criar_ticket_page.preencher_produto_sap("S4 HANA")

    # Selecionar Role SAP: "4. Outro" (value="186")
    criar_ticket_page.selecionar_role_sap("186")

    # --- 6. Clicar em Abrir Ticket ---
    print("Passo 4: Clicando em 'Abrir Ticket' para finalizar...")
    criar_ticket_page.clicar_abrir_ticket()

    # --- 7. Validação Pós-Criação ---
    # Aqui, esperamos que após a criação, a página redirecione para a HOME_URL
    # (que é a página de listagem de ocorrências).
    print("Passo 5: Validando a criação do ticket (esperando redirecionamento para a lista de ocorrências)...")
    try:
        portal_home_page.page.wait_for_url(home_url, timeout=20000) # Aumentado para 20s para garantir
        print("Redirecionamento para a página de listagem de ocorrências foi bem-sucedido.")

        # Opcional: Adicione uma validação extra para verificar se o ticket realmente aparece na lista.
        # Isso seria mais robusto. Por exemplo, procurar o texto da descrição do ticket.
        # try:
        #     expect(page.locator(f"p.help-block:has-text('{ticket_description}')")).to_be_visible(timeout=10000)
        #     print(f"Ticket com descrição '{ticket_description}' encontrado na lista!")
        # except Exception:
        #     print(f"ATENÇÃO: Ticket com descrição '{ticket_description}' NÃO encontrado na lista, mas a URL está correta.")

        print("Teste de Criação de Ticket concluído e bem-sucedido! 🎉")

    except Exception as e:
        print(f"Teste de Criação de Ticket FALHOU! ❌ Não foi possível validar a criação ou o redirecionamento. Erro: {e}")
        print(f"URL atual após clique em Abrir Ticket: {page.url}")
        # Captura de tela para ajudar na depuração em caso de falha
        screenshot_path = "criar_ticket_falhou.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot '{screenshot_path}' salvo para depuração.")
        raise # Re-levanta a exceção para que pytest marque o teste como falho

    print("--- Fim do teste de Criação de Ticket ---")