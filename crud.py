# IMPORTANDO SQLITE3

import sqlite3

# ESTABELECENDO CONEXÃO

con = sqlite3.connect('bar.db')

#CURSOR OF SQLITE3
cursor = con.cursor()

#C = CREATE OF CRUD 

def adicionar_estoque(produto, tipo, quantidade, preco, preco_venda):
    cursor.execute("INSERT INTO estoque (produto, tipo, quantidade, preco, preco_venda) VALUES (?, ?, ?, ?, ?)",(produto, tipo, quantidade, preco, preco_venda))
    con.commit()
    print(f"Produto '{produto}' adicionado com sucesso!")

#R = READ OF CRUD

def ver_estoque():
    cursor.execute("SELECT * FROM estoque")
    rows = cursor.fetchall()
    for row in rows:
        print(f'ID: {row[0]}, Produto: {row[1]}, Tipo: {row[2]}, Quantidade: {row[3]}, Preço: {row[4]}, Preço de venda: {row[5]}')

# U = UPDATE OF CRUD

def update_estoque(estoque_id, new_produto, new_tipo, new_qnd, new_preco, new_preco_venda):
    cursor.execute("UPDATE estoque SET produto = ?, tipo = ?, quantidade = ?, preco = ?, preco_venda = ? WHERE id = ?",(new_produto, new_tipo, new_qnd, new_preco, new_preco_venda, estoque_id))
    con.commit()
    print(f"Produto ID {estoque_id} Atualizado")

#D = DELETE OF CRUD
def delete_estoque(estoque_id):
    cursor.execute('DELETE FROM estoque WHERE id = ?',(estoque_id))
    con.commit()
    print(f'Produto ID {estoque_id} deletado')
