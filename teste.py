from crud import *

#con = sqlite3.connect('bar.db')
#cursor = con.cursor()

def calculando(produto):

    cursor.execute('SELECT SUM(total) FROM venda WHERE produto = ?',(produto.upper(),))
    vendas_totais = cursor.fetchone() [0] or 0
    print(f"💰 Vendas Totais: R$ {vendas_totais:.2f} do produto: {produto}")

#calculando('Skol garrafa')

#adicionar_estoque('SKOL GARRAFA', 'BEBIDA ALCOÓLICA', 20, 2.75, 4.00 )
#criar_comandas('Paulo','SKOL GARRAFA', 2, 4.00, 5/9/2025)
update_comanda('paulo','skol garrafa', 3, 4.00, 5/9/2025)

con.close()