import tkinter as tk
from tkinter import ttk, messagebox

class GuiView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
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
        self.mainloop()
    
    # --- Criação das Abas ---

    def create_products_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Produtos")
        self.setup_universal_tab(tab, "Produto", 
                                 ["ID", "Nome", "Preço", "Categoria", "Estoque", "Fornecedor"],
                                 self.controller.list_products,
                                 self.show_add_product_dialog)
        # Botão adicional para atualizar estoque
        ttk.Button(tab, text="Atualizar Estoque", command=self.show_update_stock_dialog).pack(pady=5)

    def create_sales_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Vendas")
        self.setup_universal_tab(tab, "Venda",
                                 ["ID", "Produto", "Cliente", "Qtd", "Total", "Data"],
                                 self.controller.list_sales,
                                 self.show_add_sale_dialog)


    def create_customers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Clientes")
        self.setup_universal_tab(tab, "Cliente",
                                 ["ID", "Nome", "Email", "Telefone"],
                                 self.controller.list_customers,
                                 self.show_add_customer_dialog)

    def create_suppliers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Fornecedores")
        self.setup_universal_tab(tab, "Fornecedor",
                                 ["ID", "Empresa", "Contato", "Telefone"],
                                 self.controller.list_suppliers,
                                 self.show_add_supplier_dialog)

    def create_reports_tab(self):
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
        """Função genérica para limpar e popular a treeview de relatórios."""
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
        cols = ["ID Produto", "Nome", "Estoque"]
        self.display_report(cols, self.controller.get_estoque_critico)

    def display_top_5_report(self):
        cols = ["Produto", "Total Vendido"]
        self.display_report(cols, self.controller.get_top_5_vendidos)

    def display_vendas_categoria_report(self):
        cols = ["Categoria", "Nº de Vendas", "Receita Total"]
        self.display_report(cols, self.controller.get_vendas_por_categoria)

    def display_nunca_vendidos_report(self):
        cols = ["ID Produto", "Nome", "Estoque"]
        self.display_report(cols, self.controller.get_produtos_nunca_vendidos)            

    # --- Widgets reutilizáveis ---
    
    def setup_universal_tab(self, parent_tab, entity_name, columns, list_callback, add_callback):
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
        # Limpa a árvore
        for item in tree.get_children():
            tree.delete(item)
        # Busca os novos dados e insere na árvore
        for row in list_callback():
            tree.insert("", "end", values=row)
            
    # --- Diálogos de Adição ---

    def show_add_product_dialog(self):
        fields = {"Nome": "nome", "Preço": "preco", "Categoria": "categoria", "Estoque": "estoque", "ID Fornecedor": "id_fornecedor"}
        self.create_dialog("Adicionar Produto", fields, self.controller.add_product)

    def show_add_sale_dialog(self):
        fields = {"ID Produto": "id_produto", "ID Cliente": "id_cliente", "Quantidade": "quantidade"}
        self.create_dialog("Registrar Venda", fields, self.controller.add_sale)

    def show_add_customer_dialog(self):
        fields = {"Nome": "nome", "Email": "email", "Telefone": "telefone"}
        self.create_dialog("Adicionar Cliente", fields, self.controller.add_customer)

    def show_add_supplier_dialog(self):
        fields = {"Nome da Empresa": "nome_empresa", "Contato": "contato", "Telefone": "telefone"}
        self.create_dialog("Adicionar Fornecedor", fields, self.controller.add_supplier)

    # --- Novo diálogo: Atualizar Estoque ---
    def show_update_stock_dialog(self):
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
        self.refresh_tree(self.notebook.tabs()[0].tree, self.controller.list_products)
        self.refresh_tree(self.notebook.tabs()[1].tree, self.controller.list_sales)
        self.refresh_tree(self.notebook.tabs()[2].tree, self.controller.list_customers)
        self.refresh_tree(self.notebook.tabs()[3].tree, self.controller.list_suppliers)