Teste de Abertura e Fechamento de Tcikets com Playwright
Este projeto tem como objetivo realizar automaticamente a abertura e fechamento de tickets utilizando o framework Playwright. Ele simula um usuário preenchendo as credenciais e acessando o sistema, abrindo e fechando tickets validando se tudo ocorreu como esperado.

🔧 Tecnologias Utilizadas
- Python 3.7+
- Playwright (versão Python)
- Chromium (via Playwright)

📦 Instalação

1. Clone este repositório:
bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3. Instale as dependências necessárias:
bash
pip install playwright
playwright install

🔧 Configuração:
No .env, coloque as suas credenciais.

▶️ Como Executar
Execute o script Python:
bash
pytest
O navegador será aberto em modo visível (não headless) e com ações mais lentas (slow_mo=500ms) para facilitar a visualização do processo.