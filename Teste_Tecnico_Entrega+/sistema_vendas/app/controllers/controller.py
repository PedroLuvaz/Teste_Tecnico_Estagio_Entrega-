from app.models.produto_model import ProdutoModel
from app.models.venda_model import VendaModel
from app.models.cliente_model import ClienteModel
from app.models.fornecedor_model import FornecedorModel
from app.views.cli_view import CLIView

class Controller:
    def __init__(self):
        self.produto_model = ProdutoModel()
        self.venda_model = VendaModel()
        self.cliente_model = ClienteModel()
        self.fornecedor_model = FornecedorModel()
        self.view = CLIView()

    def run(self):
        while True:
            choice = self.view.show_main_menu()
            if choice == '1': self.product_management()
            elif choice == '2': self.sales_management()
            elif choice == '3': self.customer_management()
            elif choice == '4': self.supplier_management()
            elif choice == '0': self.view.show_message("Saindo do sistema. Até logo!"); break
            else: self.view.show_message("Opção inválida. Tente novamente.")

    def product_management(self):
        while True:
            choice = self.view.show_product_menu()
            if choice == '1': self.view.show_products(self.produto_model.get_all())
            elif choice == '2':
                details = self.view.get_product_details()
                new_id = self.produto_model.create(*details)
                self.view.show_message(f"Produto '{details[0]}' criado com ID {new_id}.")
            elif choice == '3':
                pid, qtd = self.view.get_stock_update()
                success = self.produto_model.update_stock(pid, qtd)
                self.view.show_message("Estoque atualizado." if success else "Falha ao atualizar.")
            elif choice == '4':
                categoria = self.view.get_category_input()
                produtos = self.produto_model.get_by_category(categoria)
                self.view.show_products(produtos)
            elif choice == '9': break
            else: self.view.show_message("Opção inválida.")

    def sales_management(self):
        while True:
            choice = self.view.show_sales_menu()
            if choice == '1': self.view.show_sales(self.venda_model.get_all())
            elif choice == '2':
                p_id, c_id, qtd = self.view.get_new_sale_details()
                new_id, message = self.venda_model.register_sale(p_id, c_id, qtd)
                self.view.show_message(message)
            elif choice == '3':
                try:
                    inicio, fim = self.view.get_period_input()
                    vendas = self.venda_model.get_by_period(inicio, fim)
                    self.view.show_sales(vendas)
                except Exception as e:
                    self.view.show_message(f"Erro ao buscar vendas. Verifique o formato da data. Detalhe: {e}")
            elif choice == '9': break
            else: self.view.show_message("Opção inválida.")    

    def customer_management(self):
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
        while True:
            choice = self.view.show_supplier_menu()
            if choice == '1': self.view.show_suppliers(self.fornecedor_model.get_all())
            elif choice == '2':
                details = self.view.get_supplier_details()
                new_id = self.fornecedor_model.create(*details)
                self.view.show_message(f"Fornecedor '{details[0]}' criado com ID {new_id}.")
            elif choice == '9': break
            else: self.view.show_message("Opção inválida.")

    