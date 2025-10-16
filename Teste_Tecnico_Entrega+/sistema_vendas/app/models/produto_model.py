from .database import get_db_connection

class ProdutoModel:
    def get_all(self):
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            query = """
                SELECT p.id, p.nome, p.preco, p.categoria, p.estoque, f.nome_empresa
                FROM produtos p
                LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                ORDER BY p.id
            """
            cur.execute(query)
            return cur.fetchall()

    def get_by_id(self, produto_id):
        conn = get_db_connection()
        if not conn: return None
        with conn.cursor() as cur:
            query = """
                SELECT p.id, p.nome, p.preco, p.categoria, p.estoque, f.nome_empresa
                FROM produtos p
                LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                WHERE p.id = %s
            """
            cur.execute(query, (produto_id,))
            return cur.fetchone()

    def get_by_category(self, categoria):
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            # Usamos LEFT JOIN para mostrar o fornecedor e ILIKE para busca não sensível a maiúsculas
            query = """
                SELECT p.id, p.nome, p.preco, p.categoria, p.estoque, f.nome_empresa
                FROM produtos p
                LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                WHERE p.categoria ILIKE %s
                ORDER BY p.id
            """
            cur.execute(query, (f'%{categoria}%',))
            return cur.fetchall()

    def create(self, nome, preco, categoria, estoque, fornecedor_id):
        conn = get_db_connection()
        if not conn: return None
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO produtos (nome, preco, categoria, estoque, fornecedor_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (nome, preco, categoria, estoque, fornecedor_id)
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id

    def update_stock(self, produto_id, nova_quantidade):
        conn = get_db_connection()
        if not conn: return False
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE produtos SET estoque = %s WHERE id = %s",
                (nova_quantidade, produto_id)
            )
            conn.commit()
            return cur.rowcount > 0