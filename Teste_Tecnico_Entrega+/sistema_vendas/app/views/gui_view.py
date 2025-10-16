import tkinter as tk
from tkinter import ttk, messagebox

class GuiView(tk.Tk):
    """
    A classe GuiView é a janela principal da aplicação, construída com Tkinter.
    Ela herda de tk.Tk e é responsável por criar e organizar todos os widgets
    da interface gráfica, como abas, tabelas e botões.
    Ela interage com o GuiController para obter dados e executar ações.
    """
    def __init__(self, controller):
        super().__init__()
        # O controller é injetado na View para fazer a comunicação com os Models.
        self.controller = controller
        self.title("Sistema de Gerenciamento de Vendas")
        self.geometry("900x600")

        # Configura o notebook (abas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Cria as abas
        self.create_products_tab()
        self.create_sales_tab()
        self.create_customers_tab()
        self.create_suppliers_tab()
        self.create_reports_tab()

    def main(self):
        """Inicia o loop principal do Tkinter, que desenha a janela e espera por eventos."""
        self.mainloop()
    
    # --- Criação das Abas ---

    def create_products_tab(self):
        """Cria a aba 'Produtos' com uma tabela e botões de ação."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Produtos")
        self.setup_universal_tab(tab, "Produto", 
                                 ["ID", "Nome", "Preço", "Categoria", "Estoque", "Fornecedor"],
                                 self.controller.list_products,
                                 self.show_add_product_dialog)
        # Botão adicional para atualizar estoque
        ttk.Button(tab, text="Atualizar Estoque", command=self.show_update_stock_dialog).pack(pady=5)

    def create_sales_tab(self):
        """Cria a aba 'Vendas' com uma tabela e botões de ação."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Vendas")
        self.setup_universal_tab(tab, "Venda",
                                 ["ID", "Produto", "Cliente", "Qtd", "Total", "Data"],
                                 self.controller.list_sales,
                                 self.show_add_sale_dialog)


    def create_customers_tab(self):
        """Cria a aba 'Clientes' com uma tabela e botões de ação."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Clientes")
        self.setup_universal_tab(tab, "Cliente",
                                 ["ID", "Nome", "Email", "Telefone"],
                                 self.controller.list_customers,
                                 self.show_add_customer_dialog)

    def create_suppliers_tab(self):
        """Cria a aba 'Fornecedores' com uma tabela e botões de ação."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Fornecedores")
        self.setup_universal_tab(tab, "Fornecedor",
                                 ["ID", "Empresa", "Contato", "Telefone"],
                                 self.controller.list_suppliers,
                                 self.show_add_supplier_dialog)

    def create_reports_tab(self):
        """Cria a aba 'Relatórios' com botões para cada tipo de relatório e uma área de visualização."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Relatórios")

        # Frame principal
        main_frame = ttk.Frame(tab, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Frame para os botões à esquerda
        btn_frame = ttk.Frame(main_frame, padding="10")
        btn_frame.pack(side="left", fill="y")

        # Frame para a visualização à direita
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(side="right", fill="both", expand=True)
        
        # Treeview para exibir os resultados
        self.report_tree = ttk.Treeview(tree_frame)
        self.report_tree.pack(fill="both", expand=True)
        
        # Botões
        ttk.Button(btn_frame, text="Estoque Crítico", command=self.display_estoque_critico_report).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Top 5 Vendas", command=self.display_top_5_report).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Vendas por Categoria", command=self.display_vendas_categoria_report).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Nunca Vendidos", command=self.display_nunca_vendidos_report).pack(fill="x", pady=5)

    def display_report(self, columns, fetch_data_callback):
        """
        Função genérica para exibir dados de um relatório na Treeview da aba de relatórios.

        Args:
            columns (list[str]): Uma lista com os nomes das colunas para o relatório.
            fetch_data_callback (function): A função do controller que busca os dados
                                            do relatório.
        """
        # Limpa a treeview
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Limpa colunas antigas e define as novas
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=150) # Largura padrão

        # Busca e insere os novos dados
        data = fetch_data_callback()
        if not data:
            messagebox.showinfo("Relatório", "Nenhum dado encontrado para este relatório.")
        else:
            for row in data:
                self.report_tree.insert("", "end", values=row)

    def display_estoque_critico_report(self):
        """Chama a função genérica para exibir o relatório de estoque crítico."""
        cols = ["ID Produto", "Nome", "Estoque"]
        self.display_report(cols, self.controller.get_estoque_critico)

    def display_top_5_report(self):
        """Chama a função genérica para exibir o relatório de top 5 produtos vendidos."""
        cols = ["Produto", "Total Vendido"]
        self.display_report(cols, self.controller.get_top_5_vendidos)

    def display_vendas_categoria_report(self):
        """Chama a função genérica para exibir o relatório de vendas por categoria."""
        cols = ["Categoria", "Nº de Vendas", "Receita Total"]
        self.display_report(cols, self.controller.get_vendas_por_categoria)

    def display_nunca_vendidos_report(self):
        """Chama a função genérica para exibir o relatório de produtos nunca vendidos."""
        cols = ["ID Produto", "Nome", "Estoque"]
        self.display_report(cols, self.controller.get_produtos_nunca_vendidos)            

    # --- Widgets reutilizáveis ---
    
    def setup_universal_tab(self, parent_tab, entity_name, columns, list_callback, add_callback):
        """
        Cria uma estrutura de aba padronizada com botões e uma tabela (Treeview).
        Esta função é reutilizada para criar as abas de Produtos, Vendas, Clientes e Fornecedores.

        Args:
            parent_tab (ttk.Frame): O widget da aba onde os elementos serão inseridos.
            entity_name (str): O nome da entidade (ex: "Produto") para usar nos textos dos botões.
            columns (list[str]): A lista de nomes de colunas para a tabela.
            list_callback (function): A função do controller para listar os itens.
            add_callback (function): A função que abre o diálogo para adicionar um novo item.
        """
        frame = ttk.Frame(parent_tab, padding="10")
        frame.pack(fill="both", expand=True)

        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text=f"Adicionar Novo {entity_name}", command=add_callback).pack(side="left")
        ttk.Button(btn_frame, text=f"Atualizar Lista", command=lambda: self.refresh_tree(tree, list_callback)).pack(side="left", padx=10)

        # Treeview para exibir a lista
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill="both", expand=True)

        # Adiciona a treeview como um atributo do frame para poder acessá-la depois
        parent_tab.tree = tree
        
        # Carrega os dados iniciais
        self.refresh_tree(tree, list_callback)

    def refresh_tree(self, tree, list_callback):
        """
        Limpa e recarrega os dados de uma tabela (Treeview).

        Args:
            tree (ttk.Treeview): O widget da tabela a ser atualizado.
            list_callback (function): A função do controller que busca os dados atualizados.
        """
        # Limpa a árvore
        for item in tree.get_children():
            tree.delete(item)
        # Busca os novos dados e insere na árvore
        for row in list_callback():
            tree.insert("", "end", values=row)
            
    # --- Diálogos de Adição ---

    def show_add_product_dialog(self):
        """Abre um diálogo para adicionar um novo produto."""
        fields = {"Nome": "nome", "Preço": "preco", "Categoria": "categoria", "Estoque": "estoque", "ID Fornecedor": "id_fornecedor"}
        self.create_dialog("Adicionar Produto", fields, self.controller.add_product)

    def show_add_sale_dialog(self):
        """Abre um diálogo para registrar uma nova venda."""
        fields = {"ID Produto": "id_produto", "ID Cliente": "id_cliente", "Quantidade": "quantidade"}
        self.create_dialog("Registrar Venda", fields, self.controller.add_sale)

    def show_add_customer_dialog(self):
        """Abre um diálogo para adicionar um novo cliente."""
        fields = {"Nome": "nome", "Email": "email", "Telefone": "telefone"}
        self.create_dialog("Adicionar Cliente", fields, self.controller.add_customer)

    def show_add_supplier_dialog(self):
        """Abre um diálogo para adicionar um novo fornecedor."""
        fields = {"Nome da Empresa": "nome_empresa", "Contato": "contato", "Telefone": "telefone"}
        self.create_dialog("Adicionar Fornecedor", fields, self.controller.add_supplier)

    # --- Novo diálogo: Atualizar Estoque ---
    def show_update_stock_dialog(self):
        """Abre um diálogo específico para atualizar o estoque de um produto."""
        dialog = tk.Toplevel(self)
        dialog.title("Atualizar Estoque")
        dialog.geometry("320x160")

        ttk.Label(dialog, text="ID Produto:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        id_entry = ttk.Entry(dialog)
        id_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(dialog, text="Novo Estoque:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        stock_entry = ttk.Entry(dialog)
        stock_entry.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        def on_submit():
            pid = id_entry.get()
            novo = stock_entry.get()
            result, message = self.controller.update_product_stock(pid, novo)
            if result:
                messagebox.showinfo("Sucesso", message)
                self.refresh_all_tabs()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", message)

        submit_button = ttk.Button(dialog, text="Atualizar", command=on_submit)
        submit_button.grid(row=2, columnspan=2, pady=12)

    def create_dialog(self, title, fields, callback):
        """
        Cria uma janela de diálogo (Toplevel) genérica com campos de entrada e um botão de salvar.

        Args:
            title (str): O título da janela de diálogo.
            fields (dict): Um dicionário onde as chaves são os rótulos dos campos (ex: "Nome")
                           e os valores são os nomes dos parâmetros para a função de callback.
            callback (function): A função do controller que será chamada ao salvar,
                                 recebendo os valores dos campos como argumentos.
        """
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x400")
        
        entries = {}
        for i, (field, param_name) in enumerate(fields.items()):
            ttk.Label(dialog, text=f"{field}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(dialog)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[param_name] = entry
        
        def on_submit():
            # Coleta os valores dos campos de entrada
            values = {param_name: entry.get() for param_name, entry in entries.items()}
            result, message = callback(**values)
            if result:
                messagebox.showinfo("Sucesso", message)
                self.refresh_all_tabs()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", message)

        submit_button = ttk.Button(dialog, text="Salvar", command=on_submit)
        submit_button.grid(row=len(fields), columnspan=2, pady=20)
        
    def refresh_all_tabs(self):
        """Atualiza os dados de todas as tabelas em todas as abas."""
        self.refresh_tree(self.notebook.tabs()[0].tree, self.controller.list_products)
        self.refresh_tree(self.notebook.tabs()[1].tree, self.controller.list_sales)
        self.refresh_tree(self.notebook.tabs()[2].tree, self.controller.list_customers)
        self.refresh_tree(self.notebook.tabs()[3].tree, self.controller.list_suppliers)