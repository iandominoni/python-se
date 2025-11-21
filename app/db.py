"""
Módulo de persistência com SQLite.
Gerencia banco de dados para respostas do questionário.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path


class Database:
    """Gerenciador de banco de dados SQLite."""

    def __init__(self, db_path=None):
        """
        Inicializa conexão com banco de dados.

        Args:
            db_path: Caminho do arquivo .db. Se None, cria na pasta do usuário.
        """
        if db_path is None:
            # Criar na pasta de dados da aplicação, não no .exe
            app_data_dir = Path.home() / ".app_pythonse"
            app_data_dir.mkdir(exist_ok=True)
            db_path = app_data_dir / "dbhistory.db"

        self.db_path = str(db_path)
        self._initialize_db()

    def _initialize_db(self):
        """Cria tabelas se não existirem."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabela de respostas
            # Respostas: armazenar como inteiro (1=sim,0=nao) para otimização
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS respostas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    eixo TEXT NOT NULL,
                    pergunta_id INTEGER NOT NULL,
                    pergunta_texto TEXT NOT NULL,
                    resposta INTEGER NOT NULL CHECK (resposta IN (0,1)),
                    pontos INTEGER DEFAULT 0,
                    data_criacao TIMESTAMP NOT NULL,
                    avaliacao_id INTEGER,
                    FOREIGN KEY (avaliacao_id) REFERENCES avaliacoes(id)
                )
            """
            )

            # Adicionar coluna pontos se não existir (para compatibilidade com BD existente)
            cursor.execute("PRAGMA table_info(respostas)")
            columns = [col[1] for col in cursor.fetchall()]
            if "pontos" not in columns:
                cursor.execute(
                    "ALTER TABLE respostas ADD COLUMN pontos INTEGER DEFAULT 0"
                )

            # Tabela de avaliações (para agrupar respostas)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS avaliacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_paciente TEXT NOT NULL,
                    nivel_risco TEXT NOT NULL,
                    pontuacao INTEGER NOT NULL,
                    data_criacao TIMESTAMP NOT NULL
                )
            """
            )

            conn.commit()

    # MÉTODO REMOVIDO: add_resposta
    # Use save_avaliacao_with_respostas para salvar avaliação + respostas atomicamente

    def update_resposta(self, resposta_id, resposta):
        """
        Atualiza uma resposta existente.

        Args:
            resposta_id: ID da resposta
            resposta: Novo valor ("sim" ou "nao")
        """
        val = self._normalize_resposta(resposta)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE respostas 
                SET resposta = ?, data_criacao = ?
                WHERE id = ?
            """,
                (val, datetime.now(), resposta_id),
            )
            conn.commit()

    def get_respostas_by_eixo(self, eixo, avaliacao_id=None):
        """
        Obtém todas as respostas de um eixo.

        Args:
            eixo: Nome do eixo
            avaliacao_id: Se fornecido, filtra apenas dessa avaliação

        Returns:
            Lista de dicionários com respostas
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if avaliacao_id:
                cursor.execute(
                    """
                    SELECT id, eixo, pergunta_id, pergunta_texto, resposta, pontos, data_criacao
                    FROM respostas
                    WHERE eixo = ? AND avaliacao_id = ?
                    ORDER BY pergunta_id
                """,
                    (eixo, avaliacao_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, eixo, pergunta_id, pergunta_texto, resposta, pontos, data_criacao
                    FROM respostas
                    WHERE eixo = ?
                    ORDER BY pergunta_id DESC
                """,
                    (eixo,),
                )
            rows = cursor.fetchall()

            out = []
            for row in rows:
                d = dict(row)
                # converter para 'sim'/'nao'
                d["resposta"] = "sim" if d.get("resposta") == 1 else "nao"
                out.append(d)
            return out

    def get_contagem_respostas(self, eixo, avaliacao_id=None):
        """
        Obtém contagem de sim/não para um eixo.

        Args:
            eixo: Nome do eixo
            avaliacao_id: Se fornecido, filtra apenas dessa avaliação

        Returns:
            Dicionário com contagem {'sim': int, 'nao': int}
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if avaliacao_id:
                cursor.execute(
                    """
                    SELECT 
                        COALESCE(SUM(CASE WHEN resposta = 1 THEN 1 ELSE 0 END), 0) as sim,
                        COALESCE(SUM(CASE WHEN resposta = 0 THEN 1 ELSE 0 END), 0) as nao
                    FROM respostas
                    WHERE eixo = ? AND avaliacao_id = ?
                """,
                    (eixo, avaliacao_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT 
                        COALESCE(SUM(CASE WHEN resposta = 1 THEN 1 ELSE 0 END), 0) as sim,
                        COALESCE(SUM(CASE WHEN resposta = 0 THEN 1 ELSE 0 END), 0) as nao
                    FROM respostas
                    WHERE eixo = ?
                """,
                    (eixo,),
                )

            row = cursor.fetchone()
            return {"sim": row[0], "nao": row[1]} if row else {"sim": 0, "nao": 0}

    # MÉTODO REMOVIDO: add_avaliacao
    # Use save_avaliacao_with_respostas para salvar avaliação + respostas atomicamente

    def get_avaliacoes(self, limit=None, offset=0):
        """
        Obtém histórico de avaliações.

        Args:
            limit: Número máximo de registros
            offset: Deslocamento para paginação

        Returns:
            Lista de dicionários com avaliações
        """
        from datetime import datetime as dt

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if limit:
                cursor.execute(
                    """
                    SELECT id, nome_paciente, nivel_risco, pontuacao, data_criacao
                    FROM avaliacoes
                    ORDER BY data_criacao DESC
                    LIMIT ? OFFSET ?
                """,
                    (limit, offset),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, nome_paciente, nivel_risco, pontuacao, data_criacao
                    FROM avaliacoes
                    ORDER BY data_criacao DESC
                """
                )

            rows = cursor.fetchall()
            result = []
            for row in rows:
                d = dict(row)
                # Renomear campos para compatibilidade com main.py
                d["patient_name"] = d.pop("nome_paciente", "")
                d["level"] = d.pop("nivel_risco", "")
                d["score"] = d.pop("pontuacao", 0)
                # Formatar data
                data_criacao = d.pop("data_criacao", "")
                if data_criacao:
                    try:
                        data_obj = dt.fromisoformat(data_criacao)
                        d["data"] = data_obj.strftime("%d/%m/%Y %H:%M")
                    except:
                        d["data"] = data_criacao
                result.append(d)
            return result

    def get_avaliacao(self, avaliacao_id):
        """
        Obtém detalhes de uma avaliação específica.

        Args:
            avaliacao_id: ID da avaliação

        Returns:
            Dicionário com dados da avaliação
        """
        from datetime import datetime as dt

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, nome_paciente, nivel_risco, pontuacao, data_criacao
                FROM avaliacoes
                WHERE id = ?
            """,
                (avaliacao_id,),
            )

            row = cursor.fetchone()
            if row:
                d = dict(row)
                # Renomear campos para compatibilidade com main.py
                d["patient_name"] = d.pop("nome_paciente", "")
                d["level"] = d.pop("nivel_risco", "")
                d["score"] = d.pop("pontuacao", 0)
                # Formatar data
                data_criacao = d.pop("data_criacao", "")
                if data_criacao:
                    try:
                        data_obj = dt.fromisoformat(data_criacao)
                        d["data"] = data_obj.strftime("%d/%m/%Y %H:%M")
                    except:
                        d["data"] = data_criacao
                return d
            return None

    def get_respostas_avaliacao(self, avaliacao_id):
        """
        Obtém todas as respostas de uma avaliação.

        Args:
            avaliacao_id: ID da avaliação

        Returns:
            Lista de dicionários com respostas
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, eixo, pergunta_id, pergunta_texto, resposta, pontos, data_criacao
                FROM respostas
                WHERE avaliacao_id = ?
                ORDER BY pergunta_id
            """,
                (avaliacao_id,),
            )
            rows = cursor.fetchall()
            out = []
            for row in rows:
                d = dict(row)
                d["resposta"] = "sim" if d.get("resposta") == 1 else "nao"
                out.append(d)
            return out

    def get_total_avaliacoes(self):
        """Obtém total de avaliações."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM avaliacoes")
            result = cursor.fetchone()
            return result[0] if result else 0

    def clear_all_data(self):
        """Limpa todas os dados (para reset/teste)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM respostas")
            cursor.execute("DELETE FROM avaliacoes")
            conn.commit()

    def save_avaliacao_with_respostas(
        self, nome_paciente, nivel_risco, pontuacao, respostas
    ):
        """
        Salva avaliação e suas respostas em uma única transação.

        Args:
            nome_paciente, nivel_risco, pontuacao: metadados
            respostas: lista de dicts com chaves eixo_nome, question_id, pergunta_texto, resposta, pontos
        Returns:
            ID da avaliação criada
        """
        with sqlite3.connect(self.db_path) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO avaliacoes (nome_paciente, nivel_risco, pontuacao, data_criacao)
                    VALUES (?, ?, ?, ?)
                """,
                    (nome_paciente, nivel_risco, pontuacao, datetime.now()),
                )
                avaliacao_id = cursor.lastrowid

                for r in respostas:
                    val = self._normalize_resposta(r.get("resposta"))
                    cursor.execute(
                        """
                        INSERT INTO respostas (eixo, pergunta_id, pergunta_texto, resposta, pontos, data_criacao, avaliacao_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            r.get("eixo_nome"),
                            r.get("question_id"),
                            r.get("pergunta_texto"),
                            val,
                            r.get("pontos", 0),
                            datetime.now(),
                            avaliacao_id,
                        ),
                    )

                conn.commit()
                return avaliacao_id
            except Exception:
                conn.rollback()
                raise

    def delete_avaliacao(self, avaliacao_id):
        """Remove avaliação e respostas associadas."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM respostas WHERE avaliacao_id = ?", (avaliacao_id,)
            )
            cursor.execute("DELETE FROM avaliacoes WHERE id = ?", (avaliacao_id,))
            conn.commit()

    def get_orphan_avaliacoes(self):
        """Lista avaliações sem nenhuma resposta."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT a.id, a.nome_paciente, a.nivel_risco, a.pontuacao, a.data_criacao
                FROM avaliacoes a
                LEFT JOIN respostas r ON r.avaliacao_id = a.id
                WHERE r.id IS NULL
                ORDER BY a.data_criacao DESC
                """
            )
            return [dict(row) for row in cursor.fetchall()]

    # ------------------ Funções Internas ------------------
    def _normalize_resposta(self, resposta):
        """Converte diferentes formatos para inteiro 1(sim)/0(nao)."""
        if isinstance(resposta, bool):
            return 1 if resposta else 0
        if isinstance(resposta, int):
            return 1 if resposta != 0 else 0
        if isinstance(resposta, str):
            r = resposta.strip().lower()
            return 1 if r in ("sim", "s", "1", "true") else 0
        return 0
