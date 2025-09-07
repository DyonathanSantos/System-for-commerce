#Importando sqlite3
import sqlite3

# Conexão com banco de dados e criação do mesmo.

def conectar():
    return sqlite3.connect('bar.db')

# Adicionando as tabelas do banco de dados e criando o cursor.
con = conectar()
cur = con.cursor()


# TABELA DE ESTOQUE
cur.execute('CREATE TABLE IF NOT EXISTS estoque( id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL, tipo TEXT NOT NULL, quantidade INTEGER  NOT NULL, preco REAL NOT NULL, preco_venda REAL NOT NULL)')
con.commit()

#TABELA DE COMANDAS
cur.execute('CREATE TABLE IF NOT EXISTS comandas( id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, status TEXT DEFAULT "aberta" ,  data TEXT)')
con.commit()

#TABELA DE ITENS DA COMANDA
cur.execute("CREATE TABLE IF NOT EXISTS comanda_itens (id INTEGER PRIMARY KEY AUTOINCREMENT, id_comanda INTEGER, produto TEXT, quantidade INTEGER, preco REAL, FOREIGN KEY (id_comanda) REFERENCES comandas(id))")

#TABELA DE VENDAS
cur.execute('CREATE TABLE IF NOT EXISTS venda (id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL, quantidade INTGER NOT NULL, preco REAL NOT NULL, total REAL NOT NULL, data TEXT)')
con.commit()

#TABELA DE GASTOS
cur.execute('CREATE TABLE IF NOT EXISTS gastos(data TEXT NOT NULL, descricao TEXT, valor REAL NOT NULL)')
con.commit()

#FECHANDO A CONEXÃO
con.close()

