# Sistema de Gerenciamento de Vendas

Este projeto é uma solução para um teste técnico para a empresa Entrega+ que consiste em um sistema simples para gerenciamento de vendas, produtos, clientes e fornecedores. A aplicação é executada inteiramente via terminal (interface de linha de comando) e utiliza um banco de dados PostgreSQL para persistência dos dados.

1.  **Interface de Linha de Comando (CLI)**: Para uma operação rápida e direta via terminal.
2.  **Interface Gráfica de Usuário (GUI)**: Uma aplicação desktop amigável construída com a biblioteca Tkinter.

A arquitetura do projeto foi desenvolvida utilizando o padrão **MVC (Model-View-Controller)** para garantir a separação de responsabilidades, facilitando a manutenção e a escalabilidade do código.

## Funcionalidades

* **Gestão de Entidades**: Cadastrar e listar Produtos, Vendas, Clientes e Fornecedores.
* **Controle de Estoque**: A atualização do estoque é feita automaticamente ao registrar uma nova venda.
* **Geração de Relatórios**: O sistema pode gerar relatórios de negócio essenciais, como:
    * Produtos com estoque crítico.
    * Top 5 produtos mais vendidos.
    * Total de vendas e receita por categoria.
    * Produtos que nunca foram vendidos.
* **Duas Interfaces**: O usuário pode escolher entre a versão CLI ou a versão gráfica (GUI) para interagir com o sistema.

## Tecnologias Utilizadas

* **Backend**: Python 3
* **Banco de Dados**: PostgreSQL
* **Interface Gráfica (GUI)**: Tkinter (biblioteca padrão do Python)
* **Driver PostgreSQL**: `psycopg2-binary`
* **Gerenciamento de Variáveis de Ambiente**: `python-dotenv`

## Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados em sua máquina:
* [Python 3.7+](https://www.python.org/downloads/)
* [PostgreSQL](https://www.postgresql.org/download/)
* [Git](https://git-scm.com/downloads)

## Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Clonar o Repositório
```bash
ggit clone https://github.com/PedroLuvaz/Teste_Tecnico_Estagio_Entrega-.git

# Navega para o diretório raiz do projeto. 
# Todos os comandos a seguir devem ser executados de dentro deste diretório.

cd Teste_Tecnico_Estagio_Entrega-plus-
cd Teste_Tecnico_Estagio_Entrega+
```

### 2. Configurar o Ambiente Virtual e Instalar Dependências
(Certifique-se que está no diretório do projeto)

É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate

# Em caso de erro de politica utilize:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\venv\Scripts\Activate.ps1

# No macOS/Linux:
source venv/bin/activate

# Instalar as bibliotecas necessárias
pip install -r requirements.txt
```

### 3. Configurar o Banco de Dados PostgreSQL

A aplicação precisa de um usuário e um banco de dados dedicados.
(Certifique-se que está no diretório do projeto)

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
    
    -- Saia do psql
    \q
    ```
    ```sql
    -- Dê todos os privilégios do novo banco para o novo usuário
    psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE minha_loja_db TO meu_usuario;"
    psql -U postgres -c "ALTER DATABASE minha_loja_db OWNER TO meu_usuario;"

    -- Saia do psql
    \q
    ```

### 4. Configurar as Variáveis de Ambiente
(Certifique-se que está no diretório do projeto)

1.  **Renomeie o arquivo `.env.example` para `.env`** (se existir) ou crie um novo arquivo chamado `.env` na raiz do projeto.
2.  **Preencha o arquivo `.env`** com os dados do banco que você acabou de criar:
    ```ini
    DB_NAME=minha_loja_db
    DB_USER=meu_usuario
    DB_PASSWORD=minha_senha_segura
    DB_HOST=localhost
    DB_PORT=5432
    ```

### 5. Criar as Tabelas e Popular o Banco

Execute os scripts SQL para preparar o banco de dados para a aplicação. Você precisará digitar a senha do seu novo usuário. (Antes entre no diretório do projeto sistema_vendas)

```bash
# Comando para criar a estrutura das tabelas
psql -U meu_usuario -d minha_loja_bd -f database/schema.sql

# Comando para inserir os dados iniciais
psql -U meu_usuario -d minha_loja_bd -f database/seeds.sql
```

### 6. Executar a Aplicação (Escolha sua Interface)

Com tudo configurado, você pode escolher qual versão da aplicação deseja executar.

#### Opção 1: Rodar a Versão Gráfica (GUI com Tkinter)

Para uma experiência visual e amigável, execute o seguinte comando:

```bash
python main_gui.py
```
Uma janela desktop aparecerá com abas para cada funcionalidade do sistema.

#### Opção 2: Rodar a Versão de Linha de Comando (CLI)

Para uma interação rápida via terminal, execute este comando:

```bash
python main.py
```
O menu principal do sistema aparecerá diretamente no seu terminal.

## 📂 Estrutura do Projeto

```
.
├── app/
│   ├── controllers/
│   │   ├── controller.py      # Lógica para CLI
│   │   └── gui_controller.py  # Lógica para GUI
│   ├── models/
│   │   ├── ...                # Lógica de negócio e acesso ao BD
│   └── views/
│       ├── cli_view.py        # Interface do terminal
│       └── gui_view.py        # Interface gráfica com Tkinter
├── database/
│   └── ...                    # Scripts SQL
├── .env
├── main.py                    # Ponto de entrada para CLI
├── main_gui.py                # Ponto de entrada para GUI
├── ANALISE.md
└── requirements.txt
```
