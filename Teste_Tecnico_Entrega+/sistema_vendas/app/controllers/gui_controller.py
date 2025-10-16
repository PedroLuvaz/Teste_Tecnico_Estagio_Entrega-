from app.models.produto_model import ProdutoModel
from app.models.venda_model import VendaModel
from app.models.cliente_model import ClienteModel
from app.models.fornecedor_model import FornecedorModel
from app.models.relatorio_model import RelatorioModel

class GuiController:
    """
    Controller específico para a interface gráfica (GUI) com Tkinter.
    Esta classe faz a ponte entre a GuiView (a janela da aplicação) e os Models.
    Ela recebe as ações do usuário da View, processa-as usando os Models e
    retorna os dados formatados para exibição.
    """
    def __init__(self):
        self.produto_model = ProdutoModel()
        self.venda_model = VendaModel()
        self.cliente_model = ClienteModel()
        self.fornecedor_model = FornecedorModel()
        self.relatorio_model = RelatorioModel()



    # --- Funções de Listagem (para a View) ---
    def list_products(self):
        """Retorna uma lista de todos os produtos."""
        return self.produto_model.get_all()

    def list_sales(self):
        """Retorna uma lista de todas as vendas."""
        return self.venda_model.get_all()

    def list_customers(self):
        """Retorna uma lista de todos os clientes."""
        return self.cliente_model.get_all()

    def list_suppliers(self):
        """Retorna uma lista de todos os fornecedores."""
        return self.fornecedor_model.get_all()
    
    def get_estoque_critico(self):
        """Retorna produtos com estoque crítico."""
        return self.relatorio_model.get_produtos_estoque_critico()

    def get_top_5_vendidos(self):
        """Retorna os 5 produtos mais vendidos."""
        return self.relatorio_model.get_top_5_produtos_vendidos()

    def get_vendas_por_categoria(self):
        """Retorna o total de vendas agrupado por categoria."""
        return self.relatorio_model.get_total_vendas_por_categoria()

    def get_produtos_nunca_vendidos(self):
        """Retorna produtos que nunca foram vendidos."""
        return self.relatorio_model.get_produtos_nunca_vendidos()

    def get_produtos_status_critico(self):
        """Retorna produtos com status crítico (nunca vendidos ou estoque baixo)."""
        return self.relatorio_model.get_produtos_status_critico()

    def get_relatorio_vendas_completo(self):
        """Retorna o relatório de vendas com produto, categoria e data."""
        return self.venda_model.get_all()

    def get_produtos_estoque_alto(self):
        """Retorna produtos com estoque > 5, ordenados."""
        return self.relatorio_model.get_produtos_estoque_alto()
    
    def add_product(self, nome, preco, categoria, estoque, id_fornecedor):
        """
        Adiciona um novo produto ao banco de dados.

        Args:
            nome (str): Nome do produto.
            preco (str): Preço do produto (será convertido para float).
            categoria (str): Categoria do produto.
            estoque (str): Quantidade em estoque (será convertido para int).
            id_fornecedor (str): ID do fornecedor (será convertido para int).

        Returns:
            tuple[bool, str]: Uma tupla contendo um booleano de sucesso e uma mensagem.
        """
        try:
            # Validação simples
            if not all([nome, preco, categoria, estoque, id_fornecedor]):
                return False, "Todos os campos são obrigatórios."
            
            self.produto_model.create(nome, float(preco), categoria, int(estoque), int(id_fornecedor))
            return True, "Produto adicionado com sucesso!"
        except Exception as e:
            return False, f"Erro ao adicionar produto: {e}"

    def add_sale(self, id_produto, id_cliente, quantidade, data_venda=""):
        """
        Registra uma nova venda. data_venda é opcional (string ISO); se vazio usa NOW().
        Retorna (bool, mensagem).
        """
        try:
            if not all([id_produto, id_cliente, quantidade]):
                return False, "ID do produto, ID do cliente e quantidade são obrigatórios."
            pid = int(id_produto)
            cid = int(id_cliente)
            qtd = int(quantidade)

            new_id, message = self.venda_model.register_sale(pid, cid, qtd, data_venda.strip() or None)
            if new_id is None:
                return False, message
            return True, message
        except ValueError:
            return False, "IDs e quantidade devem ser números inteiros."
        except Exception as e:
            return False, f"Erro ao registrar venda: {e}"

    def add_customer(self, nome, email, telefone):
        """
        Adiciona um novo cliente.

        Args:
            nome (str): Nome do cliente.
            email (str): Email do cliente.
            telefone (str): Telefone do cliente.

        Returns:
            tuple[bool, str]: Uma tupla contendo um booleano de sucesso e uma mensagem.
        """
        try:
            if not all([nome, email, telefone]):
                return False, "Todos os campos são obrigatórios."
            
            self.cliente_model.create(nome, email, telefone)
            return True, "Cliente adicionado com sucesso!"
        except Exception as e:
            return False, f"Erro ao adicionar cliente: {e}"

    def add_supplier(self, nome_empresa, contato, telefone):
        """
        Adiciona um novo fornecedor.

        Args:
            nome_empresa (str): Nome da empresa fornecedora.
            contato (str): Nome do contato na empresa.
            telefone (str): Telefone do fornecedor.

        Returns:
            tuple[bool, str]: Uma tupla contendo um booleano de sucesso e uma mensagem.
        """
        try:
            if not all([nome_empresa, contato, telefone]):
                return False, "Todos os campos são obrigatórios."

            self.fornecedor_model.create(nome_empresa, contato, telefone)
            return True, "Fornecedor adicionado com sucesso!"
        except Exception as e:
            return False, f"Erro ao adicionar fornecedor: {e}"

    # --- Nova função: Atualizar estoque do produto ---
    def update_product_stock(self, product_id, novo_estoque):
        """
        Atualiza o estoque de um produto específico.
        Args:
            product_id (str): O ID do produto a ser atualizado.
            novo_estoque (str): A nova quantidade em estoque.
        Returns:
            tuple[bool, str]: Uma tupla contendo um booleano de sucesso e uma mensagem.
        """
        try:
            if not all([product_id, novo_estoque]):
                return False, "ID do produto e novo estoque são obrigatórios."
            pid = int(product_id)
            stock = int(novo_estoque)

            # Tenta chamar o método de atualização de estoque no model.
            if hasattr(self.produto_model, "update_stock"):
                result = self.produto_model.update_stock(pid, stock)
            elif hasattr(self.produto_model, "set_estoque"):
                result = self.produto_model.set_estoque(pid, stock)
            elif hasattr(self.produto_model, "update"):
                # método genérico update(id, **fields)
                result = self.produto_model.update(pid, estoque=stock)
            else:
                return False, "Função de atualização de estoque não implementada no model."

            # Interpreta o resultado
            if result is False or result is None:
                return False, "Não foi possível atualizar o estoque (registro não encontrado ou erro)."
            return True, "Estoque atualizado com sucesso!"
        except ValueError:
            return False, "ID do produto e estoque devem ser números inteiros."
        except Exception as e:
            return False, f"Erro ao atualizar estoque: {e}"

    # --- Novos métodos para suportar buscas na GUI ---
    def get_product_by_id(self, product_id):
        """Retorna lista com o produto (ou vazia) para popular a tree da GUI."""
        if not product_id:
            return []
        try:
            prod = self.produto_model.get_by_id(int(product_id))
            return [prod] if prod else []
        except Exception:
            return []

    def get_products_by_category(self, categoria):
        """Retorna lista de produtos filtrados por categoria (pode ser substring)."""
        if not categoria:
            return self.list_products()
        try:
            return self.produto_model.get_by_category(categoria)
        except Exception:
            return []

    def get_sales_by_period(self, inicio, fim):
        """Retorna lista de vendas dentro do período informado (strings 'YYYY-MM-DD' ou datetimes)."""
        if not inicio or not fim:
            return self.list_sales()
        try:
            return self.venda_model.get_by_period(inicio, fim)
        except Exception:
            return []