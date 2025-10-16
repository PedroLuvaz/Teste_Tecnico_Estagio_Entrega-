from .database import get_db_connection
from datetime import datetime

class VendaModel:
    def get_all(self):
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            query = """
                SELECT
                    v.id,
                    p.nome AS produto,
                    p.categoria,
                    c.nome AS cliente,
                    v.quantidade,
                    v.valor_total,
                    v.data_venda
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id
                JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.data_venda DESC
            """
            cur.execute(query)
            return cur.fetchall()

    def get_by_period(self, inicio, fim):
        """
        Busca vendas entre duas datas (inclusive). inicio/fim podem ser strings YYYY-MM-DD
        ou YYYY-MM-DD HH:MM:SS ou objetos date/datetime.
        Retorna lista de tuplas com as mesmas colunas que get_all().
        """
        conn = get_db_connection()
        if not conn: return []
        # Normaliza entradas
        try:
            if isinstance(inicio, str):
                inicio_dt = datetime.fromisoformat(inicio)
            else:
                inicio_dt = inicio
            if isinstance(fim, str):
                fim_dt = datetime.fromisoformat(fim)
            else:
                fim_dt = fim
        except Exception:
            raise

        with conn.cursor() as cur:
            query = """
                SELECT
                    v.id,
                    p.nome AS produto,
                    p.categoria,
                    c.nome AS cliente,
                    v.quantidade,
                    v.valor_total,
                    v.data_venda
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id
                JOIN clientes c ON v.cliente_id = c.id
                WHERE v.data_venda BETWEEN %s AND %s
                ORDER BY v.data_venda DESC
            """
            cur.execute(query, (inicio_dt, fim_dt))
            return cur.fetchall()

    def register_sale(self, produto_id, cliente_id, quantidade, data_venda=None):
        """
        Registra uma venda: Checa estoque, calcula valor_total (preço * quantidade),
        insere em vendas e decrementa estoque do produto. Se data_venda for fornecida
        (str ISO ou datetime), usa-a; caso contrário usa NOW().
        Retorna (new_id, message).
        """
        conn = get_db_connection()
        if not conn:
            return None, "Erro: conexão com o banco indisponível."

        # Normaliza data_venda
        dv = None
        if data_venda:
            try:
                if isinstance(data_venda, str):
                    dv = datetime.fromisoformat(data_venda)
                else:
                    dv = data_venda
            except Exception as e:
                return None, f"Erro: formato de data inválido ({e}). Use ISO: YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS"

        try:
            with conn.cursor() as cur:
                # Busca produto e estoque/preco com bloqueio para transação segura
                cur.execute("SELECT preco, estoque FROM produtos WHERE id = %s FOR UPDATE", (produto_id,))
                prod = cur.fetchone()
                if not prod:
                    conn.rollback()
                    return None, "Erro: produto não encontrado."
                preco, estoque_atual = prod
                if estoque_atual < quantidade:
                    conn.rollback()
                    return None, f"Erro: estoque insuficiente (disponível: {estoque_atual})."

                valor_total = float(preco) * int(quantidade)
                # Insere venda — usa NOW() quando dv é None, senão envia o timestamp
                if dv is None:
                    cur.execute(
                        "INSERT INTO vendas (produto_id, cliente_id, quantidade, valor_total, data_venda) VALUES (%s, %s, %s, %s, NOW()) RETURNING id",
                        (produto_id, cliente_id, quantidade, valor_total)
                    )
                else:
                    cur.execute(
                        "INSERT INTO vendas (produto_id, cliente_id, quantidade, valor_total, data_venda) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                        (produto_id, cliente_id, quantidade, valor_total, dv)
                    )
                new_id = cur.fetchone()[0]
                # Atualiza estoque
                cur.execute("UPDATE produtos SET estoque = estoque - %s WHERE id = %s", (quantidade, produto_id))
                conn.commit()
                return new_id, "Venda registrada com sucesso."
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            return None, f"Erro ao registrar venda: {e}"