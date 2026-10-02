# RetailManager-API
RetailManager API é uma API de gerenciamento comercial desenvolvida em Python, responsável pelo controle de produtos, estoque e vendas. O projeto foi criado com foco no aprendizado de lógica de programação, organização de código e construção de uma estrutura semelhante a sistemas utilizados no varejo

## Instalação

### Pré-requisitos
- Python 3.10+
- Cliente Firebird instalado na máquina (necessário para o `firebird-driver` conseguir conectar ao banco)

### Passo a passo
1. Clone o repositório e acesse a pasta do projeto:
   ```bash
   git clone <url-do-repositorio>
   cd RetailManager-API
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # Linux/Mac
   ```
3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto com a chave usada para gerar os tokens JWT:
   ```
   SECRET_KEY=sua_chave_secreta
   ```
5. Configure o arquivo `fm-api.ini` (atualmente lido em `C:/API/fm-api.ini`) com os dados de conexão do Firebird:
   ```ini
   [FIREBIRD]
   host = localhost
   port = 3050
   caminho = C:/caminho/para/banco.fdb
   usuario = SYSDBA
   senha = masterkey
   ```
6. Execute a aplicação:
   ```bash
   python app.py
   ```
