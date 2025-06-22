from playwright.sync_api import sync_playwright

def fazer_login():
    # URL do site de login
    login_url = "https://roadmaphomo.multidadosti.com.br/login.php?manual=1&lo=1"

    # URL esperada após o login bem-sucedido
    expected_post_login_url = "https://roadmaphomo.multidadosti.com.br/?display=portal&m=servicedesk&d=listarOcorrencias/views"

    # Credenciais
    usuario = "leonardo.machado"
    senha = "Inicial@123"

    with sync_playwright() as p:
        # Lançar o navegador Chromium em modo não headless
        browser = p.chromium.launch(headless=False, slow_mo=500) # slow_mo para ver as ações mais devagar
        page = browser.new_page()

        print(f"Abrindo o site de login: {login_url}")
        page.goto(login_url)

        # 1. Preencher o campo de usuário
        print(f"Preenchendo o usuário: {usuario}")
        page.fill("#login", usuario)

        # 2. Preencher o campo de senha
        print("Preenchendo a senha...")
        page.fill("#password_sem_md5", senha)

        # 3. Clicar no botão "Entrar"
        print("Clicando no botão 'Entrar'...")
        page.click("button:has-text('Entrar')")

        # **NOVA VALIDAÇÃO:** Esperar que a URL seja a esperada após o login
        try:
            print(f"Aguardando redirecionamento para: {expected_post_login_url}")
            # wait_for_url espera até que a URL corresponda ao padrão ou string fornecida
            # O timeout padrão é 30 segundos, mas você pode ajustar se necessário (ex: timeout=10000)
            page.wait_for_url(expected_post_login_url)
            print("Teste de login ocorreu como esperado!")

        except Exception as e:
            print(f"Erro: Não foi possível alcançar a URL esperada após o login. {e}")
            print("Teste de login FALHOU!")
            print(f"URL atual: {page.url}")
            # Tirar um screenshot para depuração em caso de falha
            page.screenshot(path="login_failed.png")
            print("Screenshot 'login_failed.png' salvo para debug.")

        # Fechar o navegador
        browser.close()
        print("Navegador fechado.")

if __name__ == "__main__":
    fazer_login()