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
cur.execute('CREATE TABLE IF NOT EXISTS comanda( id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, produto TEXT NOT NULL, quantidade INTEGER NOT NULL, preco_venda REAL NOT NULL, data TEXT)')
con.commit()

#TABELA DE VENDAS
cur.execute('CREATE TABLE IF NOT EXISTS venda (id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL, quantidade INTGER NOT NULL, preco_venda REAL NOT NULL, total REAL NOT NULL, data TEXT)')
con.commit()

#TABELA DE GASTOS
cur.execute('CREATE TABLE IF NOT EXISTS gastos(data TEXT NOT NULL, descricao TEXT, valor REAL NOT NULL)')
con.commit()

#FECHANDO A CONEXÃO
con.close()

