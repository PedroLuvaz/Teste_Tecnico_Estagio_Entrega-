from .database import get_db_connection
from .produto_model import ProdutoModel
from .cliente_model import ClienteModel

class VendaModel:
    def get_all(self):
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            query = """
                SELECT v.id, p.nome, c.nome, v.quantidade, v.valor_total, v.data_venda
                FROM vendas v
                LEFT JOIN produtos p ON v.produto_id = p.id
                LEFT JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.data_venda DESC
            """
            cur.execute(query)
            return cur.fetchall()

    def get_by_period(self, data_inicio, data_fim):
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            query = """
                SELECT v.id, p.nome, c.nome, v.quantidade, v.valor_total, v.data_venda
                FROM vendas v
                LEFT JOIN produtos p ON v.produto_id = p.id
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.data_venda::date BETWEEN %s AND %s
                ORDER BY v.data_venda DESC
            """
            cur.execute(query, (data_inicio, data_fim))
            return cur.fetchall()    

    def register_sale(self, produto_id, cliente_id, quantidade):
        produto_model = ProdutoModel()
        cliente_model = ClienteModel()

        produto = produto_model.get_by_id(produto_id)
        if not produto:
            return None, "Erro: Produto não encontrado."

        
        id_prod, nome_prod, preco, categoria, estoque = produto
        if estoque < quantidade:
            return None, f"Erro: Estoque insuficiente. Apenas {estoque} unidades disponíveis."

        valor_total = preco * quantidade
        novo_estoque = estoque - quantidade

        conn = get_db_connection()
        if not conn:
             return None, "Erro: Falha na conexão com o banco de dados."

        try:
            with conn.cursor() as cur:
                # Insere a nova venda
                cur.execute(
                    "INSERT INTO vendas (produto_id, cliente_id, quantidade, valor_total) VALUES (%s, %s, %s, %s) RETURNING id",
                    (produto_id, cliente_id, quantidade, valor_total)
                )
                nova_venda_id = cur.fetchone()[0]

                # Atualiza o estoque do produto
                produto_model.update_stock(produto_id, novo_estoque)

                conn.commit()
                return nova_venda_id, "Venda registrada com sucesso!"
        except Exception as e:
            if conn:
                conn.rollback()
            return None, f"Erro ao registrar venda: {e}"