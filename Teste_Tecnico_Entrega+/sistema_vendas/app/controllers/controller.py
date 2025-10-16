from app.models.produto_model import ProdutoModel
from app.models.venda_model import VendaModel
from app.models.cliente_model import ClienteModel
from app.models.fornecedor_model import FornecedorModel
from app.views.cli_view import CLIView
from app.models.relatorio_model import RelatorioModel
from datetime import datetime
from decimal import Decimal

class Controller:
    """
    A classe Controller atua como o maestro da aplicação no modo de linha de comando (CLI).
    Ela conecta a View (interação com o usuário) e os Models (lógica de negócio e dados),
    orquestrando o fluxo da aplicação.
    """
    def __init__(self):
        """
        Inicializa o Controller, instanciando todos os models necessários
        e a view de linha de comando (CLIView).
        """
        self.produto_model = ProdutoModel()
        self.venda_model = VendaModel()
        self.cliente_model = ClienteModel()
        self.fornecedor_model = FornecedorModel()
        self.relatorio_model = RelatorioModel()
        self.view = CLIView()

    def run(self):
        """
        Inicia o loop principal da aplicação. Exibe o menu principal e direciona
        o fluxo com base na escolha do usuário até que a opção de sair seja selecionada.
        """
        while True:
            choice = self.view.show_main_menu()
            if choice == '1': self.product_management()
            elif choice == '2': self.sales_management()
            elif choice == '3': self.customer_management()
            elif choice == '4': self.supplier_management()
            elif choice == '5': self.reports_management()
            elif choice == '0': self.view.show_message("Saindo do sistema. Até logo!"); break
            else: self.view.show_message("Opção inválida. Tente novamente.")

    def product_management(self):
        """
        Gerencia o submenu de produtos. Permite ao usuário listar, criar,
        atualizar estoque, filtrar produtos e buscar por ID.
        """
        while True:
            choice = self.view.show_product_menu()
            if choice == '1': self.view.show_products(self.produto_model.get_all())
            elif choice == '2':
                # Coleta os detalhes do novo produto e o cria no banco
                details = self.view.get_product_details()
                new_id = self.produto_model.create(*details)
                self.view.show_message(f"Produto '{details[0]}' criado com ID {new_id}.")
            elif choice == '3':
                # Coleta o ID do produto e a nova quantidade para atualizar o estoque
                pid, qtd = self.view.get_stock_update()
                success = self.produto_model.update_stock(pid, qtd)
                self.view.show_message("Estoque atualizado." if success else "Falha ao atualizar.")
            elif choice == '4':
                # Filtra produtos por categoria
                categoria = self.view.get_category_input()
                produtos = self.produto_model.get_by_category(categoria)
                self.view.show_products(produtos)
            elif choice == '5':
                # Busca produto por ID
                try:
                    pid = self.view.get_product_id()

                    produto = self.produto_model.get_by_id(pid)
                    if produto:
                        # Reaproveita o método de exibição (lista com um item)
                        self.view.show_products([produto])
                    else:
                        self.view.show_message(f"Produto com ID {pid} não encontrado.")
                except Exception as e:
                    self.view.show_message(f"Erro ao buscar produto por ID: {e}")
            elif choice == '9': break
            else: self.view.show_message("Opção inválida.")

    def reports_management(self):
        """
        Gerencia o submenu de relatórios. Permite ao usuário visualizar
        diferentes relatórios de negócio.
        """
        while True:
            choice = self.view.show_reports_menu()
            if choice == '1':
                # Exibe produtos com estoque baixo
                produtos = self.relatorio_model.get_produtos_estoque_critico()
                self.view.show_estoque_critico_report(produtos)
            elif choice == '2':
                # Exibe os 5 produtos mais vendidos
                produtos = self.relatorio_model.get_top_5_produtos_vendidos()
                self.view.show_top_produtos_report(produtos)
            elif choice == '3':
                # Exibe o total de vendas por categoria
                categorias = self.relatorio_model.get_total_vendas_por_categoria()
                self.view.show_vendas_categoria_report(categorias)
            elif choice == '4':
                # Exibe produtos que nunca foram vendidos
                produtos = self.relatorio_model.get_produtos_nunca_vendidos()
                self.view.show_nunca_vendidos_report(produtos)
            elif choice == '5':
                # Exibe produtos com status crítico
                produtos = self.relatorio_model.get_produtos_status_critico()
                self.view.show_status_critico_report(produtos)
            elif choice == '9':
                break
            else:
                self.view.show_message("Opção inválida.")        

    def sales_management(self):
        """
        Menu de gestão de vendas (CLI). Permite listar, registrar e buscar por período.
        Sanitiza valores retornados pelo model (Decimal -> float, datetime -> str)
        para evitar erros de formatação no CLI.
        """
        while True:
            try:
                choice = self.view.show_sales_menu()
            except AttributeError:
                # fallback se CLIView não tiver show_sales_menu
                print("\n--- Gestão de Vendas ---")
                print("1 - Listar vendas")
                print("2 - Registrar venda")
                print("3 - Buscar por período")
                print("9 - Voltar")
                choice = input("Escolha: ").strip()

            if choice == "1":
                rows = self.venda_model.get_all()
                # reutiliza a mesma exibição que o view providenciar (se existir) ou imprime simples
                if hasattr(self.view, "print_sales_rows"):
                    self.view.print_sales_rows(rows)
                else:
                    print("\n--- Todas as Vendas ---")
                    for r in rows:
                        print(r)
            elif choice == "2":
                # registrar venda via CLI (usa métodos da view se existirem)
                try:
                    pid = self.view.get_input("ID do produto: ") if hasattr(self.view, "get_input") else input("ID do produto: ")
                    cid = self.view.get_input("ID do cliente: ") if hasattr(self.view, "get_input") else input("ID do cliente: ")
                    qtd = self.view.get_input("Quantidade: ") if hasattr(self.view, "get_input") else input("Quantidade: ")
                    data = ""
                    if hasattr(self.view, "get_input"):
                        data = self.view.get_input("Data da venda (opcional, YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS): ")
                    else:
                        data = input("Data da venda (opcional, YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS): ")
                    ok, msg = self.add_sale(pid, cid, qtd) if data.strip() == "" else self.add_sale(pid, cid, qtd, data)
                    print(msg)
                except Exception as e:
                    print(f"Erro ao registrar venda: {e}")
            elif choice == "3":
                # buscar por período
                try:
                    inicio = self.view.get_input("Data de início (YYYY-MM-DD): ") if hasattr(self.view, "get_input") else input("Data de início (YYYY-MM-DD): ")
                    fim = self.view.get_input("Data de fim (YYYY-MM-DD): ") if hasattr(self.view, "get_input") else input("Data de fim (YYYY-MM-DD): ")
                    raw = self.venda_model.get_by_period(inicio.strip(), fim.strip())
                    sanitized = []
                    for row in raw or []:
                        if not row:
                            continue
                        new_row = []
                        for v in row:
                            if isinstance(v, datetime):
                                new_row.append(v.strftime("%Y-%m-%d %H:%M:%S"))
                            elif isinstance(v, Decimal):
                                new_row.append(float(v))
                            elif v is None:
                                new_row.append("")
                            else:
                                new_row.append(v)
                        # Se model retornou (id, produto, categoria, cliente, qtd, total, data) mapeia para exibição
                        if len(new_row) == 7:
                            mapped = (new_row[0], new_row[1], new_row[3], new_row[4], new_row[5], new_row[6])
                        else:
                            mapped = tuple(new_row)
                        sanitized.append(mapped)

                    if hasattr(self.view, "print_sales_rows"):
                        self.view.print_sales_rows(sanitized)
                    else:
                        print("\n--- Relatório de Vendas ---")
                        for r in sanitized:
                            print(r)
                except Exception as e:
                    print(f">> Erro ao buscar vendas. Verifique o formato da data. Detalhe: {e}")
            elif choice == "9":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def customer_management(self):
        """
        Gerencia o submenu de clientes. Permite ao usuário listar e cadastrar novos clientes.
        """
        while True:
            choice = self.view.show_customer_menu()
            if choice == '1': self.view.show_customers(self.cliente_model.get_all())
            elif choice == '2':
                details = self.view.get_customer_details()
                new_id = self.cliente_model.create(*details)
                self.view.show_message(f"Cliente '{details[0]}' criado com ID {new_id}.")
            elif choice == '9': break
            else: self.view.show_message("Opção inválida.")

    def supplier_management(self):
        """
        Gerencia o submenu de fornecedores. Permite ao usuário listar e cadastrar novos fornecedores.
        """
        while True:
            choice = self.view.show_supplier_menu()
            if choice == '1': self.view.show_suppliers(self.fornecedor_model.get_all())
            elif choice == '2':
                details = self.view.get_supplier_details()
                new_id = self.fornecedor_model.create(*details)
                self.view.show_message(f"Fornecedor '{details[0]}' criado com ID {new_id}.")
            elif choice == '9': break
            else: self.view.show_message("Opção inválida.")
