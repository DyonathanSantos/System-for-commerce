# IMPORTANDO SQLITE3

import sqlite3
from datetime import datetime

# ESTABELECENDO CONEXÃO

con = sqlite3.connect('bar.db')

#CURSOR OF SQLITE3
cursor = con.cursor()

#C = CREATE OF CRUD 

def adicionar_estoque(produto, tipo, quantidade, preco, preco_venda):
    cursor.execute("INSERT INTO estoque (produto, tipo, quantidade, preco, preco_venda) VALUES (?, ?, ?, ?, ?)",(produto.lower(), tipo.lower(), quantidade, preco, preco_venda))
    con.commit()
    print(f"Produto '{produto}' adicionado com sucesso!")

def criar_comandas (nome, produto, quantidade, preco_venda, data):

    data = datetime.now().strftime("%d-%m-%Y %H:%M")
    cursor.execute("INSERT INTO comanda (nome, produto, quantidade, preco_venda, data) VALUES (?, ?, ?, ?, ?)",(nome.upper(), produto.lower(), quantidade, preco_venda, data))
    con.commit()

#R = READ OF CRUD

def ver_estoque():
    cursor.execute("SELECT * FROM estoque")
    rows = cursor.fetchall()
    for row in rows:
        print(f'ID: {row[0]}, Produto: {row[1]}, Tipo: {row[2]}, Quantidade: {row[3]}, Preço: {row[4]}, Preço de venda: {row[5]}')

# U = UPDATE OF CRUD

def update_estoque(estoque_id, new_produto, new_tipo, new_qnd, new_preco, new_preco_venda):
    cursor.execute("UPDATE estoque SET produto = ?, tipo = ?, quantidade = ?, preco = ?, preco_venda = ? WHERE id = ?",(new_produto.lower(), new_tipo.lower(), new_qnd, new_preco, new_preco_venda, estoque_id))
    con.commit()
    print(f"Produto ID {estoque_id} Atualizado")

def fechar_comanda(nome):
    data = datetime.now().strftime("%d-%m-%Y %H:%M")
    cursor.execute("SELECT produto, quantidade, preco_venda FROM comanda WHERE nome = ?",(nome.upper(),))
    itens = cursor.fetchall()

    for produto, quantidade, preco_venda in itens:
        total = quantidade * preco_venda
        cursor.execute("INSERT INTO venda (produto, quantidade, preco_venda, total, data) VALUES (?, ?, ?, ?, ?)",(produto, quantidade, preco_venda, total, data))
        cursor.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE produto = ?",(quantidade, produto))
        cursor.execute("DELETE FROM comanda WHERE nome = ?",(nome.upper(),))
        con.commit()
    
def update_comanda(nome, new_produto, new_quantidade, preco_venda, data):
    cursor.execute("SELECT produto FROM comanda WHERE nome = ?",(nome.upper(),))
    produto_existente = cursor.fetchall()[0]
    print(produto_existente)
    if produto_existente  == [new_produto]:
        cursor.execute("UPDATE comanda SET produto = ?, quantidade = ?, preco_venda = ?, data = ? WHERE nome = ?",(new_produto.lower(), new_quantidade, preco_venda, data, nome.upper()))
        con.commit()
        print(f" ✅ A comanda do cliente {nome} foi Atualizada")
    else:
        
        criar_comandas(nome, new_produto,new_quantidade,preco_venda,data)
        con.commit()
        print(f"📋 Foi criado mais uma comanda para o novo produto do cliente {nome}!")
    


#D = DELETE OF CRUD

def delete_estoque(estoque_id):
    cursor.execute("DELETE FROM estoque WHERE id = ?",(estoque_id))
    con.commit()
    print(f'Produto ID {estoque_id} deletado')
