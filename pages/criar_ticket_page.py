# pages/criar_ticket_page.py
from playwright.sync_api import Page, expect

class CriarTicketPage:
    def __init__(self, page: Page, create_ticket_url: str):
        self.page = page
        self.create_ticket_url = create_ticket_url

        # Seletores para o formulário de criação de ticket
        self.abrir_tickets_link = page.locator("a[data-original-title='Abrir Tickets']")
        self.search_cliente_button = page.locator("button#search_cliente_icon_portal")
        self.search_projeto_button = page.locator("button#search_projeto_icon_portal")

        # Seletores para o MODAL de pesquisa (cliente/projeto)
        self.modal_dialog = page.locator("div.modal-dialog") # Seletor genérico para o modal
        self.modal_search_input = page.locator("input[placeholder='Pesquisar...'][data-filter-text]")
        self.modal_search_submit_button = page.locator("button.btn.default[type='submit'] >> i.fa-search")

        # Seletores para resultados no modal (ajustados para serem mais flexíveis)
        # Usamos locator().filter() para ser mais preciso no primeiro resultado específico
        self.first_cliente_result_brain = page.locator("button.list-group-item.margin-bottom-sm").filter(has_text="BRAIN CONSULTING").first
        self.first_projeto_result_backoffice = page.locator("button.list-group-item.margin-bottom-sm").filter(has_text="BACKOFFICE").first


        # Seletores para o formulário principal
        self.solicitacao_dropdown = page.locator("select#idProblema")
        self.descricao_textarea = page.locator("textarea#idDescricao")
        self.produto_sap_input = page.locator("input[name='campos_adicionais[hd_ocorrencias][710]']")
        self.role_sap_dropdown = page.locator("select[name='campos_adicionais[hd_ocorrencias][711]']")
        self.abrir_ticket_submit_button = page.locator("button.btn.bg-color-distinct-1:has-text('Abrir Ticket')")

    def navegar_para_formulario(self):
        """Navega para a URL direta do formulário de criação de ticket."""
        print(f"Navegando para a URL de criação de ticket: {self.create_ticket_url}")
        self.page.goto(self.create_ticket_url)
        # Espera por um elemento-chave do formulário para garantir que carregou
        self.page.wait_for_selector(self.search_cliente_button.selector, state="visible", timeout=15000)


    def abrir_form_via_link(self):
        """Clica no link 'Abrir Tickets' na página inicial."""
        print("Clicando no link 'Abrir Tickets' na página inicial...")
        self.abrir_tickets_link.click()
        self.page.wait_for_url(self.create_ticket_url, timeout=10000)


    def selecionar_cliente(self, cliente_nome: str):
        """Abre o modal de seleção de cliente, pesquisa e seleciona."""
        print(f"Iniciando seleção de cliente: {cliente_nome}")
        self.search_cliente_button.click()

        # **ESPERA 1: Esperar o modal aparecer e o campo de pesquisa estar visível**
        print("Aguardando modal de cliente e campo de pesquisa...")
        self.modal_search_input.wait_for(state="visible", timeout=10000) # Espera 10s

        print(f"Preenchendo pesquisa no modal com: {cliente_nome}")
        self.modal_search_input.fill(cliente_nome)

        print("Clicando no botão de pesquisa do modal...")
        self.modal_search_submit_button.click()

        # **ESPERA 2: Esperar o resultado da pesquisa aparecer**
        print(f"Aguardando 'BRAIN CONSULTING' aparecer nos resultados...")
        self.first_cliente_result_brain.wait_for(state="visible", timeout=10000) # Espera 10s

        print("Clicando no primeiro resultado do cliente 'BRAIN CONSULTING'...")
        self.first_cliente_result_brain.click()

        # **ESPERA 3: Esperar o modal fechar**
        print("Aguardando o modal de cliente fechar...")
        self.modal_search_input.wait_for(state="hidden", timeout=10000) # Espera 10s

    def selecionar_projeto(self, projeto_nome: str):
        """Abre o modal de seleção de projeto, pesquisa (se necessário) e seleciona."""
        print(f"Iniciando seleção de projeto: {projeto_nome}")
        self.search_projeto_button.click()

        # **ESPERA 1: Esperar o modal aparecer e o campo de pesquisa estar visível**
        print("Aguardando modal de projeto e campo de pesquisa...")
        self.modal_search_input.wait_for(state="visible", timeout=10000) # Pode ser o mesmo modal, mas reloaded

        # Se precisar pesquisar aqui também:
        # Pela sua descrição, parece que não precisa pesquisar, apenas clicar no primeiro após abrir o modal.
        # Se precisar:
        # print(f"Preenchendo pesquisa no modal com: {projeto_nome}")
        # self.modal_search_input.fill(projeto_nome)
        # print("Clicando no botão de pesquisa do modal...")
        # self.modal_search_submit_button.click()

        # **ESPERA 2: Esperar o resultado do projeto aparecer**
        print(f"Aguardando 'BACKOFFICE' aparecer nos resultados...")
        self.first_projeto_result_backoffice.wait_for(state="visible", timeout=10000) # Espera 10s

        print("Clicando no primeiro resultado do projeto 'BACKOFFICE'...")
        self.first_projeto_result_backoffice.click()

        # **ESPERA 3: Esperar o modal fechar**
        print("Aguardando o modal de projeto fechar...")
        self.modal_search_input.wait_for(state="hidden", timeout=10000) # Espera 10s

    def selecionar_solicitacao(self, valor: str):
        """Seleciona uma opção no dropdown 'Solicitação'."""
        print(f"Selecionando solicitação: {valor}")
        self.solicitacao_dropdown.select_option(value=valor)

    def preencher_descricao(self, descricao: str):
        """Preenche o campo de descrição do ticket."""
        print(f"Preenchendo descrição: '{descricao}'")
        # **ATENÇÃO AQUI:** Se o textarea estiver oculto (display:none) e for gerenciado por um editor WYSIWYG,
        # 'fill' pode não funcionar. Você pode precisar interagir com o elemento visível do editor.
        # Por exemplo, se for um iframe, você teria que mudar o frame antes.
        # Por enquanto, mantemos o fill direto.
        self.descricao_textarea.fill(descricao)

    def preencher_produto_sap(self, produto: str):
        """Preenche o campo de produto SAP."""
        print(f"Preenchendo produto SAP: {produto}")
        self.produto_sap_input.fill(produto)

    def selecionar_role_sap(self, valor: str):
        """Seleciona uma opção no dropdown 'Role SAP'."""
        print(f"Selecionando Role SAP: {valor}")
        self.role_sap_dropdown.select_option(value=valor)

    def clicar_abrir_ticket(self):
        """Clica no botão 'Abrir Ticket'."""
        print("Clicando no botão 'Abrir Ticket' para finalizar...")
        self.abrir_ticket_submit_button.click()
        # Não adicionamos espera de URL aqui, pois a validação deve ser feita no teste
        # para ser mais flexível (pode ser um toast, uma mudança de URL, etc.).