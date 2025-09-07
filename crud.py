# IMPORTANDO SQLITE3

import sqlite3
from datetime import datetime

# ESTABELECENDO CONEXÃO

con = sqlite3.connect('bar.db')

#CURSOR OF SQLITE3
cursor = con.cursor()

#C = CREATE OF CRUD -------------------------------------------------------------------------------

def adicionar_estoque(produto, tipo, quantidade, preco, preco_venda): #check
    cursor.execute("INSERT INTO estoque (produto, tipo, quantidade, preco, preco_venda) VALUES (?, ?, ?, ?, ?)",(produto.lower(), tipo.lower(), quantidade, preco, preco_venda))
    con.commit()
    print(f"Produto '{produto}' adicionado com sucesso!")
    con.close()

def abrir_comanda (nome,data): #check

    data = datetime.now().strftime("%d-%m-%Y %H:%M")
    cursor.execute("INSERT INTO comandas (nome, data) VALUES (?, ?)",(nome.upper(),data))
    con.commit()
    comanda_id = cursor.lastrowid
    print(f"✅ Comanda {comanda_id} aberta para {nome}")
    con.close()
    return comanda_id

#R = READ OF CRUD -------------------------------------------------------------------------------

def ver_estoque(): #check
    cursor.execute("SELECT * FROM estoque")
    rows = cursor.fetchall()
    for row in rows:
        print(f'ID: {row[0]}, Produto: {row[1]}, Tipo: {row[2]}, Quantidade: {row[3]}, Preço: R$ {row[4]}, Preço de venda: R$ {row[5]}')

    con.close()


def listar_comandas_abertas(): #check
    cursor.execute("SELECT id,nome, status, data FROM comandas WHERE status = 'aberta'")
    comandas = cursor.fetchall()

    if comandas:
        print("📋 Comandas abertas:")
        for id_comanda, nome, status, data in comandas:
            print(f"- ID: {id_comanda} | Cliente: {nome} | Status: {status} | Data: {data}")

    else:
            print("✅ Nenhuma comanda aberta no momento.")

    con.close()
    return

#LISTAR ITENS DE UMA COMANDA ESPECÍFICA

def listar_itens_comanda(id_comanda): #check
    cursor.execute("SELECT produto, quantidade, preco FROM comanda_itens WHERE id_comanda = ?",(id_comanda,))
    itens = cursor.fetchall()
 
    if itens:
        print(f"🧾 Itens da comanda {id_comanda}:")

        for produto, quantidade, preco in itens:
            print(f"- {produto} x {quantidade} = R${quantidade * preco:.2f}")
        
        
    else:
        print(f"⚠️ Nenhum item encontrado na comanda {id_comanda}")

    con.close()
    return itens

# U = UPDATE OF CRUD -------------------------------------------------------------------------------------

#Atualizando estoque
def update_estoque(estoque_id, new_produto, new_tipo, new_qnd, new_preco, new_preco_venda): #check
    cursor.execute("UPDATE estoque SET produto = ?, tipo = ?, quantidade = ?, preco = ?, preco_venda = ? WHERE id = ?",(new_produto.lower(), new_tipo.lower(), new_qnd, new_preco, new_preco_venda, estoque_id))
    con.commit()
    print(f"Produto ID {estoque_id} Atualizado")
    con.close()

#ATUALIZANDO COMANDAS
def atualizar_comandas (id_comanda, produto, quantidade, preco): #CHECK

    cursor.execute("SELECT id, quantidade FROM comanda_itens WHERE id_comanda = ? AND produto = ?",(id_comanda, produto.lower()))
    item = cursor.fetchone()

    if item:
        novo_total = item[1] + quantidade
        cursor.execute("UPDATE comanda_itens SET quantidade = ? WHERE id = ?",(novo_total, item[0]))
        print(f"🔄 Atualizado: {produto} agora tem {novo_total} unidades na comanda {id_comanda}")
    else:
        cursor.execute("INSERT INTO comanda_itens (id_comanda, produto, quantidade, preco) VALUES(?, ?, ?, ?)",(id_comanda, produto.lower(), quantidade, preco))
        print(f"✅ Adicionado: {produto} x{quantidade} na comanda {id_comanda}")

    con.commit()
    con.close()

#FECHANDO COMANDAS
def fechar_comanda(id_comanda): #check
    data = datetime.now().strftime("%d-%m-%Y %H:%M")
    cursor.execute("SELECT produto, quantidade, preco FROM comanda_itens WHERE id_comanda = ?", (id_comanda,))
    itens = cursor.fetchall()
    con.close()

    for produto, quantidade, preco in itens:
        total = quantidade * preco
        cursor.execute("INSERT INTO venda (produto, quantidade, preco, total, data) VALUES (?, ?, ?, ?, ?)",(produto, quantidade, preco, total, data))
        cursor.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE produto = ?",(quantidade, produto))
        cursor.execute("UPDATE comandas SET status = 'fechada' WHERE id = ? ",(id_comanda,))
        con.commit()
    print(f" ❌ Comanda com ID : {id_comanda} foi fechada!")
    con.close()




#D = DELETE OF CRUD ----------------------------------------------------------------------------------------------

def delete_estoque(estoque_id):  #check
    cursor.execute("DELETE FROM estoque WHERE id = ?",(estoque_id,))
    con.commit()
    print(f'Produto ID {estoque_id} deletado')
    con.close()

def comanda_clear(id_comanda): #check
    cursor.execute("DELETE FROM comanda_itens WHERE id_comanda = ?",(id_comanda,))
    con.commit()
    print("Itens limpados com sucesso")
    con.close()

def vendas_clear_all():
    cursor.execute("DELETE FROM venda")
    con.commit()
    print("Vendas apagadas")
    con.close()

def vendas_clear_select(venda_id):
    cursor.execute("DELETE FROM venda WHERE id = ?",(venda_id,))
    con.commit()
    con.close()

