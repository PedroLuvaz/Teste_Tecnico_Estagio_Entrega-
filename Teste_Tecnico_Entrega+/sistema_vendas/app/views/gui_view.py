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
        # Busca por ID e filtro por categoria
        search_frame = ttk.Frame(tab)
        search_frame.pack(fill="x", pady=5)

        ttk.Label(search_frame, text="Buscar por ID:").pack(side="left", padx=(0,4))
        id_entry = ttk.Entry(search_frame, width=10)
        id_entry.pack(side="left")
        def on_search_id():
            pid = id_entry.get().strip()
            data = self.controller.get_product_by_id(pid)
            self._populate_tree(tab.tree, data)
        ttk.Button(search_frame, text="Buscar", command=on_search_id).pack(side="left", padx=6)

        ttk.Label(search_frame, text="Filtrar por Categoria:").pack(side="left", padx=(12,4))
        cat_entry = ttk.Entry(search_frame, width=20)
        cat_entry.pack(side="left")
        def on_filter_cat():
            cat = cat_entry.get().strip()
            data = self.controller.get_products_by_category(cat)
            self._populate_tree(tab.tree, data)
        ttk.Button(search_frame, text="Filtrar", command=on_filter_cat).pack(side="left", padx=6)

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
        # Filtro por período
        period_frame = ttk.Frame(tab)
        period_frame.pack(fill="x", pady=5)

        ttk.Label(period_frame, text="Início (YYYY-MM-DD):").pack(side="left", padx=(0,4))
        start_entry = ttk.Entry(period_frame, width=12)
        start_entry.pack(side="left")
        ttk.Label(period_frame, text="Fim (YYYY-MM-DD):").pack(side="left", padx=(8,4))
        end_entry = ttk.Entry(period_frame, width=12)
        end_entry.pack(side="left")
        def on_search_period():
            inicio = start_entry.get().strip()
            fim = end_entry.get().strip()
            try:
                data = self.controller.get_sales_by_period(inicio, fim)
                # adapta linhas caso o model retorne categoria extra
                rows = []
                for r in data:
                    if not r: continue
                    rlist = list(r)
                    # modelo pode ser (id, produto, categoria, cliente, qtd, total, data)
                    # mapear para (ID, Produto, Cliente, Qtd, Total, Data)
                    if len(rlist) == 7:
                        mapped = (rlist[0], rlist[1], rlist[3], rlist[4], rlist[5], rlist[6])
                    else:
                        mapped = tuple(rlist)
                    rows.append(mapped)
                self._populate_tree(tab.tree, rows)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar vendas: {e}")
        ttk.Button(period_frame, text="Buscar por Período", command=on_search_period).pack(side="left", padx=8)

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
        ttk.Button(btn_frame, text="Status Crítico", command=self.display_status_critico_report).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Relatório de Vendas", command=self.display_relatorio_vendas_completo).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Estoque > 5", command=self.display_produtos_estoque_alto).pack(fill="x", pady=5)

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
            self.report_tree.column(col, width=120, anchor="w")

        # Busca e insere os novos dados
        data = fetch_data_callback()
        if not data:
            messagebox.showinfo("Relatório", "Nenhum registro encontrado.")
        else:
            for row in data:
                vals = list(row) if row else []
                # Ajusta tamanho para colunas
                if len(vals) > len(columns):
                    vals = vals[:len(columns)]
                else:
                    vals += [""] * (len(columns) - len(vals))
                self.report_tree.insert("", "end", values=vals)

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

    def display_status_critico_report(self):
        """Chama a função genérica para exibir o relatório de produtos com status crítico."""
        cols = ["ID Produto", "Nome", "Estoque", "Status"]
        self.display_report(cols, self.controller.get_produtos_status_critico)

    def display_relatorio_vendas_completo(self):
        """Exibe o relatório completo de vendas, incluindo categoria e data."""
        cols = ["ID Venda", "Produto", "Categoria", "Cliente", "Qtd", "Total", "Data"]
        self.display_report(cols, self.controller.get_relatorio_vendas_completo)

    def display_produtos_estoque_alto(self):
        """Exibe o relatório de produtos com estoque > 5, ordenados."""
        cols = ["ID", "Nome", "Categoria", "Preço", "Estoque"]
        self.display_report(cols, self.controller.get_produtos_estoque_alto)

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
            tree.column(col, width=120, anchor="w")
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
            vals = list(row) if row else []
            cols = tree["columns"]
            if len(vals) > len(cols):
                vals = vals[:len(cols)]
            else:
                vals += [""] * (len(cols) - len(vals))
            tree.insert("", "end", values=vals)

    def _populate_tree(self, tree, data_rows):
        """Popula diretamente uma tree com uma lista de tuplas/lists (útil para buscas)."""
        for item in tree.get_children():
            tree.delete(item)
        for row in data_rows or []:
            vals = list(row) if row else []
            cols = tree["columns"]
            if len(vals) > len(cols):
                vals = vals[:len(cols)]
            else:
                vals += [""] * (len(cols) - len(vals))
            tree.insert("", "end", values=vals)

    # --- Diálogos de Adição ---

    def show_add_product_dialog(self):
        """Abre um diálogo para adicionar um novo produto."""
        fields = {"Nome": "nome", "Preço": "preco", "Categoria": "categoria", "Estoque": "estoque", "ID Fornecedor": "id_fornecedor"}
        self.create_dialog("Adicionar Produto", fields, self.controller.add_product)

    def show_add_sale_dialog(self):
        """Abre um diálogo para registrar uma nova venda (agora com campo de data opcional)."""
        fields = {
            "ID Produto": "id_produto",
            "ID Cliente": "id_cliente",
            "Quantidade": "quantidade",
            "Data da Venda (opcional, ISO YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS)": "data_venda"
        }
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
            pid = id_entry.get().strip()
            novo = stock_entry.get().strip()
            success, msg = self.controller.update_product_stock(pid, novo)
            if success:
                messagebox.showinfo("Sucesso", msg)
                # atualiza todas as abas para refletir mudança
                self.refresh_all_tabs()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", msg)

        submit_button = ttk.Button(dialog, text="Atualizar", command=on_submit)
        submit_button.grid(row=2, columnspan=2, pady=12)

    def create_dialog(self, title, fields, callback):
        """Cria um diálogo genérico de inserção que chama callback com os valores (ordem definida por fields.values())."""
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.transient(self)
        dialog.grab_set()

        entries = {}
        r = 0
        for label_text, key in fields.items():
            ttk.Label(dialog, text=label_text + ":").grid(row=r, column=0, padx=8, pady=6, sticky="w")
            ent = ttk.Entry(dialog, width=30)
            ent.grid(row=r, column=1, padx=8, pady=6, sticky="ew")
            entries[key] = ent
            r += 1

        def on_submit():
            args = [entries[k].get().strip() for k in fields.values()]
            try:
                result = callback(*args)
                # callback deve retornar (bool, mensagem) para a GUI
                if isinstance(result, tuple) and len(result) == 2:
                    ok, msg = result
                    if ok:
                        messagebox.showinfo("Sucesso", msg)
                        self.refresh_all_tabs()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Erro", msg)
                else:
                    # caso callback seja do tipo que retorna id (CLI models), apenas informar e fechar
                    messagebox.showinfo("Resultado", str(result))
                    self.refresh_all_tabs()
                    dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao processar: {e}")

        submit_btn = ttk.Button(dialog, text="Confirmar", command=on_submit)
        submit_btn.grid(row=r, columnspan=2, pady=10)

    def refresh_all_tabs(self):
        """Atualiza todas as treeviews das abas abertas (quando houver)."""
        for child in self.notebook.winfo_children():
            tree = getattr(child, "tree", None)
            if tree:
                # tenta descobrir o callback usado originalmente lendo um atributo; se não houver, apenas recarrega produtos/sales conforme tab text
                tab_text = self.notebook.tab(child, option="text")
                if tab_text == "Produtos":
                    self.refresh_tree(tree, self.controller.list_products)
                elif tab_text == "Vendas":
                    self.refresh_tree(tree, self.controller.list_sales)
                elif tab_text == "Clientes":
                    self.refresh_tree(tree, self.controller.list_customers)
                elif tab_text == "Fornecedores":
                    self.refresh_tree(tree, self.controller.list_suppliers)