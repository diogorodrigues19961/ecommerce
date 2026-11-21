
import sqlite3

conexao = sqlite3.connect("banco.db")

cursor = conexao.cursor()

cursor.execute("""
    SELECT id, nome, email, criado_em
    FROM clientes
""")

clientes = cursor.fetchall()

for cliente in clientes:
    print(cliente)

conexao.close()
