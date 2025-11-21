import sqlite3
from pathlib import Path

# Caminho seguro para o DB
db_path = str(Path.home() / ".app_pythonse" / "dbhistory.db")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print(f"\n📂 Lendo banco: {db_path}\n")

# 1 — listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = [t[0] for t in cursor.fetchall()]

if not tabelas:
    print("Nenhuma tabela encontrada.")
    exit()

for tabela in tabelas:
    print(f"==============================")
    print(f"📌 Tabela: {tabela}")
    print(f"==============================")

    # 2 — listar colunas
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [col[1] for col in cursor.fetchall()]
    print("→ Colunas:", ", ".join(colunas))

    # 3 — listar linhas
    cursor.execute(f"SELECT * FROM {tabela}")
    linhas = cursor.fetchall()

    if not linhas:
        print("(sem registros)\n")
        continue

    print(f"→ {len(linhas)} registro(s):")
    for row in linhas:
        print(dict(row))
    print()
