class CLIView:
    def show_message(self, message):
        print(f"\n>> {message}\n")

    def show_main_menu(self):
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
        print("\n--- Gestão de Produtos ---"); print("1. Listar todos\n2. Criar novo\n3. Atualizar estoque\n9. Voltar")
        return input("Escolha uma opção: ")

    def show_sales_menu(self):
        print("\n--- Gestão de Vendas ---")
        print("1. Listar todas\n2. Registrar nova venda\n3. Buscar por período\n9. Voltar")
        return input("Escolha uma opção: ")
    
    def get_period_input(self):
        print("Digite o período no formato AAAA-MM-DD.")
        data_inicio = input("Data de início: ")
        data_fim = input("Data de fim: ")
        return data_inicio, data_fim
    
    def show_customer_menu(self):
        print("\n--- Gestão de Clientes ---"); print("1. Listar todos\n2. Cadastrar novo\n9. Voltar")
        return input("Escolha uma opção: ")

    def show_supplier_menu(self):
        print("\n--- Gestão de Fornecedores ---"); print("1. Listar todos\n2. Cadastrar novo\n9. Voltar")
        return input("Escolha uma opção: ")

    # --- Funções de Exibição (SHOW) ---
    def show_products(self, produtos):
        if not produtos: self.show_message("Nenhum produto encontrado."); return
        print("\n--- Lista de Produtos ---")
        for p in produtos: print(f"ID: {p[0]}, Nome: {p[1]}, Preço: R${p[2]:.2f}, Estoque: {p[4]}, Fornecedor: {p[5] or 'N/A'}")

    def show_sales(self, vendas):
        if not vendas: self.show_message("Nenhuma venda encontrada."); return
        print("\n--- Relatório de Vendas ---")
        for v in vendas: print(f"ID: {v[0]}, Produto: {v[1]}, Cliente: {v[2]}, Qtd: {v[3]}, Total: R${v[4]:.2f}, Data: {v[5].strftime('%d/%m/%Y %H:%M')}")

    def show_customers(self, clientes):
        if not clientes: self.show_message("Nenhum cliente encontrado."); return
        print("\n--- Lista de Clientes ---")
        for c in clientes: print(f"ID: {c[0]}, Nome: {c[1]}, Email: {c[2]}, Telefone: {c[3]}")

    def show_suppliers(self, fornecedores):
        if not fornecedores: self.show_message("Nenhum fornecedor encontrado."); return
        print("\n--- Lista de Fornecedores ---")
        for f in fornecedores: print(f"ID: {f[0]}, Empresa: {f[1]}, Contato: {f[2]}, Telefone: {f[3]}")

    def show_product_menu(self):
        print("\n--- Gestão de Produtos ---")
        print("1. Listar todos\n2. Criar novo\n3. Atualizar estoque\n4. Filtrar por categoria\n9. Voltar") # Adicionado opção 4
        return input("Escolha uma opção: ")
    
    def show_reports_menu(self):
        print("\n--- Módulo de Relatórios ---")
        print("1. Produtos com Estoque Crítico (< 5 unidades)")
        print("2. Top 5 Produtos Mais Vendidos")
        print("3. Total de Vendas por Categoria")
        print("4. Produtos Nunca Vendidos")
        print("9. Voltar ao menu principal")
        return input("Escolha uma opção: ")
    
    # MÉTODO COMPLETAMENTE NOVO
    def show_reports_menu(self):
        print("\n--- Módulo de Relatórios ---")
        print("1. Produtos com Estoque Crítico (< 5 unidades)")
        print("2. Top 5 Produtos Mais Vendidos")
        print("3. Total de Vendas por Categoria")
        print("4. Produtos Nunca Vendidos")
        print("9. Voltar ao menu principal")
        return input("Escolha uma opção: ")

    # FUNÇÕES DE EXIBIÇÃO DE RELATÓRIOS (NOVAS)
    def show_estoque_critico_report(self, produtos):
        print("\n--- RELATÓRIO: PRODUTOS COM ESTOQUE CRÍTICO ---")
        if not produtos: self.show_message("Nenhum produto com estoque crítico encontrado."); return
        for p in produtos: print(f"ID: {p[0]}, Nome: {p[1]}, Estoque Atual: {p[2]}")

    def show_top_produtos_report(self, produtos):
        print("\n--- RELATÓRIO: TOP 5 PRODUTOS MAIS VENDIDOS ---")
        if not produtos: self.show_message("Nenhuma venda registrada para gerar o relatório."); return
        for i, p in enumerate(produtos): print(f"{i+1}º Lugar - Nome: {p[0]}, Total Vendido: {p[1]} unidades")

    def show_vendas_categoria_report(self, categorias):
        print("\n--- RELATÓRIO: VENDAS TOTAIS POR CATEGORIA ---")
        if not categorias: self.show_message("Nenhuma venda registrada para gerar o relatório."); return
        for c in categorias: print(f"Categoria: {c[0]}, Vendas: {c[1]}, Receita Total: R${c[2]:.2f}")

    def show_nunca_vendidos_report(self, produtos):
        print("\n--- RELATÓRIO: PRODUTOS NUNCA VENDIDOS ---")
        if not produtos: self.show_message("Todos os produtos possuem ao menos uma venda registrada."); return
        for p in produtos: print(f"ID: {p[0]}, Nome: {p[1]}, Estoque: {p[2]}")

    def get_category_input(self):
        return input("Digite a categoria que deseja filtrar: ")
    
    # --- Funções de Captura (GET) ---
    def get_product_details(self):
        nome = input("Nome do produto: ")
        preco = float(input("Preço: "))
        categoria = input("Categoria: ")
        estoque = int(input("Estoque inicial: "))
        fornecedor_id = int(input("ID do Fornecedor: "))
        return nome, preco, categoria, estoque, fornecedor_id

    def get_new_sale_details(self):
        produto_id = int(input("ID do produto vendido: "))
        cliente_id = int(input("ID do cliente que está comprando: "))
        quantidade = int(input("Quantidade vendida: "))
        return produto_id, cliente_id, quantidade

    def get_stock_update(self):
        produto_id = int(input("ID do produto para atualizar o estoque: "))
        nova_quantidade = int(input("Nova quantidade em estoque: "))
        return produto_id, nova_quantidade
    
    def get_customer_details(self):
        nome = input("Nome do cliente: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        return nome, email, telefone

    def get_supplier_details(self):
        nome_empresa = input("Nome da empresa: ")
        contato = input("Nome do contato: ")
        telefone = input("Telefone: ")
        return nome_empresa, contato, telefone