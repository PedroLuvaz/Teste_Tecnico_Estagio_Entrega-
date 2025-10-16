from .database import get_db_connection

class RelatorioModel:
    """
    Model responsável por agrupar consultas complexas e gerar relatórios
    para a análise de negócio.
    """
    def get_produtos_estoque_critico(self, limite=5):
        """
        Retorna produtos cujo estoque está abaixo de um determinado limite.

        Args:
            limite (int, optional): O nível de estoque considerado crítico. Defaults to 5.

        Returns:
            list[tuple]: Uma lista de tuplas, onde cada tupla representa um produto
                         (id, nome, estoque).
        """
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, estoque FROM produtos WHERE estoque < %s ORDER BY estoque ASC", (limite,))
            return cur.fetchall()

    def get_top_5_produtos_vendidos(self):
        """
        Retorna o TOP 5 de produtos mais vendidos, com base na quantidade total vendida.

        Returns:
            list[tuple]: Uma lista de tuplas (nome_produto, total_vendido).
        """
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            query = """
                SELECT p.nome, SUM(v.quantidade) AS total_vendido
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id
                GROUP BY p.nome
                ORDER BY total_vendido DESC
                LIMIT 5;
            """
            cur.execute(query)
            return cur.fetchall()

    def get_total_vendas_por_categoria(self):
        """
        Calcula o número de vendas e a receita total para cada categoria de produto.

        Returns:
            list[tuple]: Uma lista de tuplas (categoria, numero_de_vendas, receita_total).
        """
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            query = """
                SELECT
                    p.categoria,
                    COUNT(v.id) AS numero_de_vendas,
                    SUM(v.valor_total) AS receita_total
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id
                GROUP BY p.categoria
                ORDER BY receita_total DESC;
            """
            cur.execute(query)
            return cur.fetchall()

    def get_produtos_nunca_vendidos(self):
        """
        Identifica e retorna todos os produtos que não possuem nenhum registro de venda.

        Returns:
            list[tuple]: Uma lista de tuplas, onde cada tupla representa um produto (id, nome, estoque).
        """
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            query = """
                SELECT p.id, p.nome, p.estoque
                FROM produtos p
                LEFT JOIN vendas v ON p.id = v.produto_id
                WHERE v.id IS NULL;
            """
            cur.execute(query)
            return cur.fetchall()