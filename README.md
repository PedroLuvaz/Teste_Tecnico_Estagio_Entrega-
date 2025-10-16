# Sistema de Gerenciamento de Vendas

Este projeto é uma solução para um teste técnico para a empresa Entrega+ que consiste em um sistema simples para gerenciamento de vendas, produtos, clientes e fornecedores. A aplicação é executada inteiramente via terminal (interface de linha de comando) e utiliza um banco de dados PostgreSQL para persistência dos dados.

A arquitetura do projeto foi desenvolvida utilizando o padrão **MVC (Model-View-Controller)** para garantir a separação de responsabilidades, facilitando a manutenção e a escalabilidade do código.

## ✨ Funcionalidades

* **Gestão de Produtos**: Listar, cadastrar e atualizar estoque de produtos.
* **Gestão de Vendas**: Registrar novas vendas (com atualização automática de estoque) e listar o histórico.
* **Gestão de Clientes**: Cadastrar e listar clientes.
* **Gestão de Fornecedores**: Cadastrar e listar fornecedores.
* **Interface via Linha de Comando**: Interação com o sistema através de um menu interativo no terminal.

## 🛠️ Tecnologias Utilizadas

* **Backend**: Python 3
* **Banco de Dados**: PostgreSQL
* **Driver PostgreSQL**: `psycopg2-binary`
* **Gerenciamento de Variáveis de Ambiente**: `python-dotenv`

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados em sua máquina:
* [Python 3.7+](https://www.python.org/downloads/)
* [PostgreSQL](https://www.postgresql.org/download/)
* [Git](https://git-scm.com/downloads)

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Clonar o Repositório
```bash
git clone https://github.com/PedroLuvaz/Teste_Tecnico_Estagio_Entrega-.git
```

### 2. Configurar o Ambiente Virtual e Instalar Dependências

É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate

# Instalar as bibliotecas necessárias
pip install -r requirements.txt
```

### 3. Configurar o Banco de Dados PostgreSQL

A aplicação precisa de um usuário e um banco de dados dedicados.

1.  **Acesse o psql como superusuário:**
    ```bash
    psql -U postgres
    ```
    
    (Você precisará digitar a senha do usuário `postgres` definida durante a instalação)

2.  **Execute os seguintes comandos SQL para criar o usuário e o banco:**
    ```sql
    -- Crie um usuário (role) para a aplicação com uma senha segura
    CREATE ROLE meu_usuario WITH LOGIN PASSWORD 'minha_senha_segura';

    -- Crie o banco de dados
    CREATE DATABASE minha_loja_db;

    -- Dê todos os privilégios do novo banco para o novo usuário
    GRANT ALL PRIVILEGES ON DATABASE minha_loja_db TO meu_usuario;

    -- Saia do psql
    \q
    ```

### 4. Configurar as Variáveis de Ambiente

1.  **Renomeie o arquivo `.env.example` para `.env`** (se existir) ou crie um novo arquivo chamado `.env` na raiz do projeto.
2.  **Preencha o arquivo `.env`** com os dados do banco que você acabou de criar:
    ```ini
    DB_NAME=minha_loja_bd
    DB_USER=meu_usuario
    DB_PASSWORD=minha_senha_segura
    DB_HOST=localhost
    DB_PORT=5432
    ```

### 5. Criar as Tabelas e Popular o Banco

Execute os scripts SQL para preparar o banco de dados para a aplicação. Você precisará digitar a senha do seu novo usuário.

```bash
# Comando para criar a estrutura das tabelas
psql -U meu_usuario -d minha_loja_bd -f database/schema.sql

# Comando para inserir os dados iniciais
psql -U meu_usuario -d minha_loja_bd -f database/seeds.sql
```

### 6. Executar a Aplicação

Com tudo configurado, inicie a aplicação com o seguinte comando:

```bash
python main.py
```

O menu principal do sistema de gerenciamento de vendas aparecerá no seu terminal, pronto para ser utilizado.

## 📂 Estrutura do Projeto

```
.
├── app/
│   ├── controllers/
│   │   └── controller.py
│   ├── models/
│   │   ├── cliente_model.py
│   │   ├── database.py
│   │   ├── fornecedor_model.py
│   │   ├── produto_model.py
│   │   └── venda_model.py
│   └── views/
│       └── cli_view.py
├── database/
│   ├── queries.sql
│   ├── schema.sql
│   └── seeds.sql
├── .env
├── main.py
├── ANALISE.md
└── requirements.txt
```
