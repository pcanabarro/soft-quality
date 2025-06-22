from playwright.sync_api import Page, expect

class CriarTicketPage:
    def __init__(self, page: Page, create_ticket_url: str):
        self.page = page
        self.create_ticket_url = create_ticket_url

        # Botões para abrir modais
        self.search_cliente_button = page.locator("button#search_cliente_icon_portal")
        self.search_projeto_button = page.locator("button#search_projeto_icon_portal")

        # Modal visível no DOM
        self.modal_dialog = self.page.locator("div.modal.fade.in")
        self.modal_search_input = self.modal_dialog.locator("input[data-filter-text]")

        # Resultados de cliente/projeto
        self.first_cliente_result_brain = page.locator("button.list-group-item.margin-bottom-sm").filter(has_text="BRAIN CONSULTING").first
        self.first_projeto_result_backoffice = page.locator("button.list-group-item.margin-bottom-sm").filter(has_text="BACKOFFICE").first

        # Campos do formulário
        self.solicitacao_dropdown = page.locator("select#idProblema")
        self.produto_sap_input = page.locator("input[name='campos_adicionais[hd_ocorrencias][710]']")
        self.role_sap_dropdown = page.locator("select[name='campos_adicionais[hd_ocorrencias][711]']")
        self.abrir_ticket_submit_button = page.locator("button.btn.bg-color-distinct-1:has-text('Abrir Ticket')")

    def navegar_para_formulario(self):
        print(f"Navegando para a URL de criação de ticket: {self.create_ticket_url}")
        self.page.goto(self.create_ticket_url)
        self.search_cliente_button.wait_for(state="visible", timeout=15000)

    def selecionar_cliente(self, cliente_nome: str):
        print(f"Iniciando seleção de cliente: {cliente_nome}")
        self.search_cliente_button.click()
        self.page.wait_for_timeout(1000)
        self.modal_dialog.wait_for(state="visible", timeout=20000)
        self.modal_search_input.wait_for(state="visible", timeout=10000)
        self.modal_search_input.type(cliente_nome, delay=100)
        resultado = self.page.locator("button.list-group-item.margin-bottom-sm").filter(has_text=cliente_nome).first
        resultado.wait_for(state="visible", timeout=15000)
        resultado.click()
        self.modal_dialog.wait_for(state="hidden", timeout=10000)

    def selecionar_projeto(self, projeto_nome: str):
        print(f"Iniciando seleção de projeto: {projeto_nome}")
        self.search_projeto_button.click()
        self.page.wait_for_timeout(1000)
        self.modal_dialog.wait_for(state="visible", timeout=20000)
        self.modal_search_input.wait_for(state="visible", timeout=10000)
        self.modal_search_input.type(projeto_nome, delay=100)
        resultado = self.page.locator("button.list-group-item.margin-bottom-sm").filter(has_text=projeto_nome).first
        resultado.wait_for(state="visible", timeout=15000)
        resultado.click()
        self.modal_dialog.wait_for(state="hidden", timeout=10000)

    def selecionar_solicitacao(self, valor: str):
        print(f"Selecionando solicitação: {valor}")
        self.solicitacao_dropdown.wait_for(state="visible", timeout=10000)
        self.solicitacao_dropdown.select_option(value=valor)

    def preencher_descricao(self, descricao: str):
        print(f"Preenchendo descrição (via TinyMCE): '{descricao}'")
        iframe = self.page.frame_locator("iframe#idDescricao_ifr")
        body = iframe.locator("body")
        print("Aguardando body do iframe estar visível...")
        body.wait_for(state="visible", timeout=10000)
        body.click()
        body.fill(descricao)

    def preencher_produto_sap(self, produto: str):
        print(f"Preenchendo produto SAP: {produto}")
        self.produto_sap_input.wait_for(state="visible", timeout=10000)
        self.produto_sap_input.fill(produto)

    def selecionar_role_sap(self, valor: str):
        print(f"Selecionando Role SAP: {valor}")
        self.role_sap_dropdown.wait_for(state="visible", timeout=10000)
        self.role_sap_dropdown.select_option(value=valor)

    def clicar_abrir_ticket(self):
        print("Clicando no botão 'Abrir Ticket' para finalizar...")
        self.abrir_ticket_submit_button.wait_for(state="visible", timeout=10000)
        self.abrir_ticket_submit_button.click()
