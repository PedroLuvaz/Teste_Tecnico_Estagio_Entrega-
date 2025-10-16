from app.models.produto_model import ProdutoModel
from app.models.venda_model import VendaModel
from app.models.cliente_model import ClienteModel
from app.models.fornecedor_model import FornecedorModel
from app.views.cli_view import CLIView
from app.models.relatorio_model import RelatorioModel

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
        atualizar estoque e filtrar produtos.
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
            elif choice == '9':
                break
            else:
                self.view.show_message("Opção inválida.")        

    def sales_management(self):
        """
        Gerencia o submenu de vendas. Permite ao usuário listar todas as vendas,
        registrar uma nova venda e buscar vendas por período.
        """
        while True:
            choice = self.view.show_sales_menu()
            if choice == '1': self.view.show_sales(self.venda_model.get_all())
            elif choice == '2':
                # Coleta os detalhes da nova venda e a registra
                p_id, c_id, qtd = self.view.get_new_sale_details()
                new_id, message = self.venda_model.register_sale(p_id, c_id, qtd)
                self.view.show_message(message)
            elif choice == '3':
                # Busca vendas dentro de um intervalo de datas
                try:
                    inicio, fim = self.view.get_period_input()
                    vendas = self.venda_model.get_by_period(inicio, fim)
                    self.view.show_sales(vendas)
                except Exception as e:
                    self.view.show_message(f"Erro ao buscar vendas. Verifique o formato da data. Detalhe: {e}")
            elif choice == '9': break
            else: self.view.show_message("Opção inválida.")    

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

    