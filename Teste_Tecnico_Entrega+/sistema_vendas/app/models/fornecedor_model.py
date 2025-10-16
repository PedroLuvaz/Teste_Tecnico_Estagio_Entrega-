from .database import get_db_connection

class FornecedorModel:
    def get_all(self):
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome_empresa, contato, telefone FROM fornecedores ORDER BY id")
            return cur.fetchall()

    def create(self, nome_empresa, contato, telefone):
        conn = get_db_connection()
        if not conn: return None
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO fornecedores (nome_empresa, contato, telefone) VALUES (%s, %s, %s) RETURNING id",
                (nome_empresa, contato, telefone)
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id