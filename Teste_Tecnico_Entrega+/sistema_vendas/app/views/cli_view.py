class CLIView:
    """
    A classe CLIView é responsável por toda a interação com o usuário via terminal.
    Ela exibe menus, solicita dados e mostra resultados, mas não contém lógica de negócio.
    """
    def show_message(self, message):
        """Exibe uma mensagem formatada para o usuário."""
        print(f"\n>> {message}\n")

    def show_main_menu(self):
        """Exibe o menu principal e retorna a escolha do usuário."""
        print("\n--- Sistema de Gerenciamento de Vendas ---")
        print("1. Gestão de Produtos")
        print("2. Gestão de Vendas")
        print("3. Gestão de Clientes")
        print("4. Gestão de Fornecedores")
        print("5. Gerar Relatórios")
        print("0. Sair")
        return input("Escolha uma opção: ")

    # --- Menus Específicos ---
    def show_product_menu(self):
        """Exibe o menu de gestão de produtos e retorna a escolha do usuário."""
        print("\n--- Gestão de Produtos ---")
        print("1 - Listar produtos")
        print("2 - Adicionar produto")
        print("3 - Atualizar estoque")
        print("4 - Filtrar por categoria")
        print("5 - Buscar por ID")    # <- opção adicionada
        print("9 - Voltar")
        return input("Escolha: ").strip()

    def show_sales_menu(self):
        """Exibe o menu de gestão de vendas e retorna a escolha."""
        print("\n--- Gestão de Vendas ---")
        print("1. Listar todas\n2. Registrar nova venda\n3. Buscar por período\n9. Voltar")
        return input("Escolha uma opção: ")
    
    def get_period_input(self):
        """Solicita e retorna um período (data de início e fim) ao usuário."""
        print("Digite o período no formato AAAA-MM-DD.")
        data_inicio = input("Data de início: ")
        data_fim = input("Data de fim: ")
        return data_inicio, data_fim
    
    def show_customer_menu(self):
        """Exibe o menu de gestão de clientes e retorna a escolha."""
        print("\n--- Gestão de Clientes ---"); print("1. Listar todos\n2. Cadastrar novo\n9. Voltar")
        return input("Escolha uma opção: ")

    def show_supplier_menu(self):
        """Exibe o menu de gestão de fornecedores e retorna a escolha."""
        print("\n--- Gestão de Fornecedores ---"); print("1. Listar todos\n2. Cadastrar novo\n9. Voltar")
        return input("Escolha uma opção: ")

    # --- Funções de Exibição (SHOW) ---
    def show_products(self, produtos):
        """Exibe uma lista de produtos de forma formatada."""
        if not produtos: self.show_message("Nenhum produto encontrado."); return
        print("\n--- Lista de Produtos ---")
        for p in produtos: print(f"ID: {p[0]}, Nome: {p[1]}, Preço: R${p[2]:.2f}, Estoque: {p[4]}, Fornecedor: {p[5] or 'N/A'}")

    def show_sales(self, vendas):
        """Exibe uma lista de vendas de forma formatada."""
        if not vendas: self.show_message("Nenhuma venda encontrada."); return
        print("\n--- Relatório de Vendas ---")
        for v in vendas: print(f"ID: {v[0]}, Produto: {v[1]}, Cliente: {v[2]}, Qtd: {v[3]}, Total: R${v[4]:.2f}, Data: {v[5].strftime('%d/%m/%Y %H:%M')}")

    def show_customers(self, clientes):
        """Exibe uma lista de clientes de forma formatada."""
        if not clientes: self.show_message("Nenhum cliente encontrado."); return
        print("\n--- Lista de Clientes ---")
        for c in clientes: print(f"ID: {c[0]}, Nome: {c[1]}, Email: {c[2]}, Telefone: {c[3]}")

    def show_suppliers(self, fornecedores):
        """Exibe uma lista de fornecedores de forma formatada."""
        if not fornecedores: self.show_message("Nenhum fornecedor encontrado."); return
        print("\n--- Lista de Fornecedores ---")
        for f in fornecedores: print(f"ID: {f[0]}, Empresa: {f[1]}, Contato: {f[2]}, Telefone: {f[3]}")

    def show_reports_menu(self):
        """Exibe o menu de relatórios e retorna a escolha do usuário."""
        print("\n--- Módulo de Relatórios ---")
        print("1. Produtos com Estoque Crítico (< 5 unidades)")
        print("2. Top 5 Produtos Mais Vendidos")
        print("3. Total de Vendas por Categoria")
        print("4. Produtos Nunca Vendidos")
        print("9. Voltar ao menu principal")
        return input("Escolha uma opção: ")
    
    def show_reports_menu(self):
        print("\n--- Módulo de Relatórios ---")
        print("1. Produtos com Estoque Crítico (< 5 unidades)")
        print("2. Top 5 Produtos Mais Vendidos")
        print("3. Total de Vendas por Categoria")
        print("4. Produtos Nunca Vendidos")
        print("9. Voltar ao menu principal")
        return input("Escolha uma opção: ")

    # FUNÇÕES DE EXIBIÇÃO DE RELATÓRIOS
    def show_estoque_critico_report(self, produtos):
        """Exibe o relatório de produtos com estoque crítico."""
        print("\n--- RELATÓRIO: PRODUTOS COM ESTOQUE CRÍTICO ---")
        if not produtos: self.show_message("Nenhum produto com estoque crítico encontrado."); return
        for p in produtos: print(f"ID: {p[0]}, Nome: {p[1]}, Estoque Atual: {p[2]}")

    def show_top_produtos_report(self, produtos):
        """Exibe o relatório dos 5 produtos mais vendidos."""
        print("\n--- RELATÓRIO: TOP 5 PRODUTOS MAIS VENDIDOS ---")
        if not produtos: self.show_message("Nenhuma venda registrada para gerar o relatório."); return
        for i, p in enumerate(produtos): print(f"{i+1}º Lugar - Nome: {p[0]}, Total Vendido: {p[1]} unidades")

    def show_vendas_categoria_report(self, categorias):
        """Exibe o relatório de vendas totais por categoria."""
        print("\n--- RELATÓRIO: VENDAS TOTAIS POR CATEGORIA ---")
        if not categorias: self.show_message("Nenhuma venda registrada para gerar o relatório."); return
        for c in categorias: print(f"Categoria: {c[0]}, Vendas: {c[1]}, Receita Total: R${c[2]:.2f}")

    def show_nunca_vendidos_report(self, produtos):
        """Exibe o relatório de produtos que nunca foram vendidos."""
        print("\n--- RELATÓRIO: PRODUTOS NUNCA VENDIDOS ---")
        if not produtos: self.show_message("Todos os produtos possuem ao menos uma venda registrada."); return
        for p in produtos: print(f"ID: {p[0]}, Nome: {p[1]}, Estoque: {p[2]}")

    def get_category_input(self):
        """Solicita e retorna o nome de uma categoria para filtro."""
        return input("Digite a categoria que deseja filtrar: ")
    
    # --- Funções de Captura (GET) ---
    def get_product_details(self):
        """Solicita e retorna os detalhes para a criação de um novo produto."""
        nome = input("Nome do produto: ")
        preco = float(input("Preço: "))
        categoria = input("Categoria: ")
        estoque = int(input("Estoque inicial: "))
        fornecedor_id = int(input("ID do Fornecedor: "))
        return nome, preco, categoria, estoque, fornecedor_id

    def get_new_sale_details(self):
        """Solicita e retorna os detalhes para registrar uma nova venda."""
        produto_id = int(input("ID do produto vendido: "))
        cliente_id = int(input("ID do cliente que está comprando: "))
        quantidade = int(input("Quantidade vendida: "))
        return produto_id, cliente_id, quantidade

    def get_stock_update(self):
        """Solicita e retorna os dados para atualização de estoque de um produto."""
        produto_id = int(input("ID do produto para atualizar o estoque: "))
        nova_quantidade = int(input("Nova quantidade em estoque: "))
        return produto_id, nova_quantidade
    
    def get_customer_details(self):
        """Solicita e retorna os detalhes para cadastrar um novo cliente."""
        nome = input("Nome do cliente: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        return nome, email, telefone

    def get_supplier_details(self):
        """Solicita e retorna os detalhes para cadastrar um novo fornecedor."""
        nome_empresa = input("Nome da empresa: ")
        contato = input("Nome do contato: ")
        telefone = input("Telefone: ")
        return nome_empresa, contato, telefone
    
    def get_product_id(self):
        """Solicita ao usuário o ID do produto. Retorna string vazia se cancelado."""
        try:
            return input("Informe o ID do produto (ou Enter para cancelar): ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return ""

    def get_product_category(self):
        """Solicita ao usuário a categoria (ou substring) para filtragem."""
        try:
            return input("Informe a categoria (ou parte dela) para filtrar (ou Enter para cancelar): ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return ""

    def get_new_stock(self):
        """Solicita o novo valor de estoque. Retorna string (vazia se cancelado)."""
        try:
            return input("Informe o novo estoque (número) (ou Enter para cancelar): ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return ""