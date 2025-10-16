from .database import get_db_connection

class ClienteModel:
    def get_all(self):
        conn = get_db_connection()
        if not conn: return []
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, email, telefone FROM clientes ORDER BY id")
            return cur.fetchall()

    def create(self, nome, email, telefone):
        conn = get_db_connection()
        if not conn: return None
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s) RETURNING id",
                (nome, email, telefone)
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id