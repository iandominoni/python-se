import sqlite3

conn = sqlite3.connect("/home/iandominoni/.app_pythonse/dbhistory.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM avaliacoes")
print("Avaliações:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM respostas")
print("Respostas:", cursor.fetchone()[0])

cursor.execute(
    "SELECT id, nome_paciente, nivel_risco, pontuacao FROM avaliacoes ORDER BY id DESC LIMIT 5"
)
print("\nÚltimas 5 avaliações:")
for row in cursor.fetchall():
    print(f"  ID {row[0]}: {row[1]} - {row[2]} ({row[3]} pts)")

cursor.execute(
    """
    SELECT a.id, a.nome_paciente, COUNT(r.id) as num_respostas
    FROM avaliacoes a
    LEFT JOIN respostas r ON a.id = r.avaliacao_id
    GROUP BY a.id
    ORDER BY a.id DESC
    LIMIT 5
"""
)
print("\nÚltimas 5 com contagem de respostas:")
for row in cursor.fetchall():
    print(f"  Avaliação {row[0]} ({row[1]}): {row[2]} respostas")

conn.close()
