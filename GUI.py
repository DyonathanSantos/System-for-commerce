#ARQUIVO PARA INTERFACE DO PROJETO 

#IMPORTAÇÃO DAS BIBLIOTECAS + O CRUD
from crud import *
import sqlite3
import pandas as pd
import streamlit as st

con = sqlite3.connect('bar.db')
cursor = con.cursor()



st.set_page_config(page_title="Bar & Adega", layout="wide")
st.title("🍺 Bar & Adega - Sistema de Controle")

# Menu lateral
menu = st.sidebar.radio("📌 Menu", ["Home","Cadastrar Produto no Estoque", "Vendas individuais","Listar Estoque","Nova Comanda", "Comandas","Adicionando Itens na comanda","Consultar comanda", "Fechando comanda","Apagar","Vendas",])

# ------------------------
# HOME
# ------------------------

if menu == "Home":
   st.markdown("""
    ## 🎉 Bem-vindo ao Sistema Bar & Adega

    Este sistema foi criado para facilitar o **gerenciamento do estoque, comandas e vendas** do bar.  
    Use o menu lateral para navegar entre as opções e manter tudo organizado.
    """)

    # --- Resumos ---
   col1, col2, col3 = st.columns(3)

    # Total de produtos no estoque
   df_estoque = ver_estoque()
   total_produtos = len(df_estoque) if not df_estoque.empty else 0

    # Total de comandas abertas
   df_comandas = listar_comandas_abertas()
   total_comandas = len(df_comandas) if not df_comandas.empty else 0

    # Total vendido (exemplo: soma do campo 'Total' das comandas fechadas)
   df_vendas = pd.read_sql_query("""
            SELECT SUM(quantidade * preco) as total_vendido
            FROM comanda_itens
            WHERE id_comanda IN (SELECT id FROM comandas WHERE status = 'fechada')
        """,con)

   total_vendido = df_vendas["total_vendido"].iloc[0] if df_vendas["total_vendido"].iloc[0] else 0

    # Mostrar nos cards
   col1.metric("📦 Produtos no Estoque", total_produtos)
   col2.metric("🧾 Comandas Abertas", total_comandas)
   col3.metric("💰 Total Vendido", f"R$ {total_vendido:.2f}")

# ------------------------
# CADASTRAR
# ------------------------

if menu == "Cadastrar Produto no Estoque":

    st.subheader("Cadastrar novo produto no estoque")

    produto = st.text_input("Nome do Produto")
    tipo = st.text_input("Categoria")
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    preco = st.number_input("Preço de Compra", min_value=0.0, step=0.05)
    preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01)

    if st.button("Salvar Produto"):
        if produto and tipo and quantidade:
            adicionar_estoque(produto, tipo, quantidade, preco, preco_venda)
            st.success(f"✅ Produto '{produto}' cadastrado com sucesso!")
        else:
            st.error("❌ Preencha todos os campos antes de salvar.")

    if st.button("Atulizar estoque"):
       if produto and preco_venda and quantidade:
          update_estoque(produto,tipo, quantidade, preco, preco_venda)
          st.success(f"✅ Produto '{produto}' atualizado com sucesso!")
       else:
          st.error("❌ Preencha todos os campos antes de atualizar")

# ------------------------
# VENDAS INDIVIDUAIS
# ------------------------
elif menu == "Vendas individuais":
   st.subheader("Adicionar vendas sem comanda")

   produto = st.text_input("Produto")
   quantidade = st.number_input("Quantidede", min_value=0, step= 1)
   preco = st.number_input("Preço", min_value=0.00, step= 0.05)
   total = st.number_input("Total", min_value= 0.0, step= 0.05)
   data = st.text_input("Data")

   if st.button("Lançar venda"):  
    if produto and quantidade and preco:
        criar_venda(produto,quantidade,preco,total,data)
        st.success(f"Venda registrada com sucesso!")
    else:
        print("Por favor preencher os campos!")


# ------------------------
# LISTAR
# ------------------------
elif menu == "Listar Estoque":
    
    st.subheader("📋 Produtos Cadastrados")
    df = ver_estoque()

    if st.button("Ver estoque"):
        if df.empty:
            st.info("Nenhum produto cadastrado ainda.")
        else:
            st.dataframe(df)

# ------------------------
# CRIAR COMANDA
# ------------------------

elif menu == "Nova Comanda":
  
  st.subheader("Abrir comanda")

  nome = st.text_input("Nome do cliente")
  data = st.text_input('Data')

  if st.button("Criar Comanda"):
      if nome and data:
        abrir_comanda(nome,data)
        st.success(f"✅ Comanda criada com sucesso do cliente {nome}!")

      else:
          st.error("❌ Preencha todos os campos antes de criar a comanda.") 

# ------------------------
# COMANDA ABERTAS
# ------------------------

elif menu == "Comandas":
 
  st.subheader("Comandas Abertas")
  df = listar_comandas_abertas()

  if st.button('Ver comandas'):  
    if df.empty:
        st.info("Nenhuma comanda aberta ainda.")
    else:
        st.dataframe(df, use_container_width=True)


# ------------------------
# ADICIONANDO ITENS
# ------------------------

elif menu == "Adicionando Itens na comanda":
   
   st.subheader("Adicionar itens")

   id_comanda = st.number_input("ID do cliente", min_value=0, step=1)
   produto = st.text_input("Produto")
   quantidade = st.number_input("Quantidade",min_value= 0, step=1)
   preco = st.number_input("Preço",min_value=0.0, step= 0.05)

   if st.button("Adicionar"):
      if id_comanda and quantidade and produto:
         atualizar_comandas(id_comanda,produto,quantidade,preco)
         st.success(f"✅ Item {produto} adicionado com sucesso!")
      else:
          st.error("❌ Preencha todos os campos antes de criar a comanda.")

# ------------------------
# ITENS DE UMA COMANDA ESPECÍFICA
# ------------------------

elif menu == "Consultar comanda":
   
    st.subheader("Ver os itens da comanda de um cliente")
    id_comanda = st.number_input("Digite o ID da comanda do cliente que deseja ver os itens",min_value=0,step=1)

    if st.button("Listar itens"):
       df = listar_itens_comanda(id_comanda)

       if df.empty:
            st.warning(f"⚠️ Nenhum item encontrado na comanda {id_comanda}")
       else:
           st.subheader(f"🧾 Itens da Comanda {id_comanda}")
           st.dataframe(df)  # ou st.dataframe(df)
           st.metric("💰 Total da Comanda", f"R$ {df['Total'].sum():.2f}") 
        
    st.info("Para encontra o ID volte no menu Comandas e procure pelo nome do cliente, assim que achar terá um número a esquerda, este é o ID!")
    
        
# ------------------------
# FECHANDO COMANDA
# ------------------------

elif menu == "Fechando comanda":
   
   st.subheader("Fechar uma Comanda")
   id_comanda = st.number_input("Digite o ID", min_value= 0, step= 1)

   if st.button("FECHAR"):
      if id_comanda:
         fechar_comanda(id_comanda)
         st.success(f"Comanda de ID {id_comanda} foi fechada!")
      else:
         st.erro("Coloque o ID do cliente!!")


# ------------------------
# APAGAR
# ------------------------
elif menu == "Apagar":
   st.subheader("Concertar erros")

   id_number = st.number_input("Digite o ID", min_value= 0, step= 1)

   if st.button("Limpar um item do estoque"):
      delete_estoque(id_number)
      st.success(f"O item {id_number} apagado com sucesso!")
   elif st.button("Apagar item de comanda"):
      comanda_clear(id_number)
      st.success(f"O item {id_number} apagado com sucesso!")
   elif st.button("Excluir comanda"):
      comanda_delete(id_number)
      st.success(f"O item {id_number} apagado com sucesso!")
   elif  st.button('Excluir venda'):
      vendas_clear_select()
   elif st.button('EXCLUIR VENDAS!!'):
      vendas_clear_all()
      st.success(f"O item {id_number} apagado com sucesso!")
   else:
      st.error('COLOQUE O ID QUE DESEJA APAGAR!')  



# ------------------------
# VENDAS
# ------------------------
elif menu == "Vendas":
    st.subheader("📊 Vendas")

    df = vendas_see()
    if df.empty:
        st.info("Cadastre produtos para ver o resumo.")
    else:
       st.dataframe(df)