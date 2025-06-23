# 🧪 Teste de Abertura e Fechamento de Tickets com Playwright

Este projeto tem como objetivo realizar automaticamente a **abertura e fechamento de tickets** utilizando o framework **Playwright**. Ele simula um usuário preenchendo as credenciais, acessando o sistema, abrindo e fechando tickets, validando se tudo ocorreu como esperado.

---

## 🔧 Tecnologias Utilizadas

- Python 3.7+
- Playwright (versão Python)
- Chromium (via Playwright)

---

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/pcanabarro/soft-quality.git
cd seu-repositorio
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências necessárias:
```bash
pip install playwright
playwright install
```

---

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com suas credenciais de acesso. Exemplo:
```
USERNAME=seu_usuario
PASSWORD=sua_senha
```

---

## ▶️ Como Executar

Execute o script com o `pytest`:

```bash
pytest
```

O navegador será aberto **em modo visível** (não headless) e com **ações mais lentas** (`slow_mo=500ms`) para facilitar a visualização do processo.

---

## 📝 Observações

- Certifique-se de que as URLs e seletores utilizados no script estejam atualizados conforme o sistema utilizado.
- O projeto pode ser expandido para incluir mais testes automatizados, como edição de tickets, verificação de logs, entre outros.
