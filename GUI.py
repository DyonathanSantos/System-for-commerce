#ARQUIVO PARA INTERFACE DO PROJETO 

#IMPORTAÇÃO DAS BIBLIOTECAS + O CRUD
from crud import *
import sqlite3
import pandas as pd
import streamlit as st


con = sqlite3.connect('bar.db',check_same_thread=False)

st.set_page_config(page_title="Bar & Adega", layout="wide")
st.title("🍺 Bar & Adega - Sistema de Controle")

# Menu lateral
menu = st.sidebar.radio("📌 Menu", ["Home","Cadastrar Produto no Estoque", "Listar Estoque","Nova Comanda", "Comandas","Itens da comanda", "Resumo",])

# ------------------------
# HOME
# ------------------------

if menu == "Home":
    st.markdown("""
    ### Introdução
    Olá, seja bem-vindo ao sistema de controle do Bar & Adega!

    O sistema foi feito para melhorar a agilidade do gerenciamento do local, afim de evitar possíveis complicações para o cliente e para o funcionário,
    no canto superior esquerdo tem uma seta para abrir o menu lateral, com isso aparecerá 5 menus, ambos com suas respectivas funções, vai ser explicado
    abaixo cada.


    ### O que você pode fazer:
    - 📦 **Cadastrar produtos** no estoque
    - 📋 **Listar produtos** e ver quantidades
    - 📊 **Ver resumo financeiro**
    - 🖊️ **Gerenciar comandas**

    ---
    ## 👈 Use o menu lateral para navegar pelo sistema.



    ---
    **Cadastrar produtos**: Neste menu vai ser para cadastrar novos produtos ou já existentes, no banco de dados do sistema, para cadastrar é preencher as informações correspondentes
    ao seus espaços.

    **Listar produtos**: Assim que cadastrar pode já visualiza-lo no menu listar produtos, tanto ver a quantidade, preço e tipo do produto, ao selecionar temos a opção de apagar o produto
    para adicionar outro ou se for descontinuada a sua venda.

    **Resumo financeiro**: Aqui vamos ter o controle de gastos e ver quanto lucramos, para assim reenvestir no negócio. (Vai ser implementado futuramente filtro para vermos qual produto vende mais e o que menos vende)

    **Gerenciar comandas**: Gerenciamento de comandas, criar-las, fecha-las e modifica-las.

    """)

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
# LISTAR
# ------------------------
elif menu == "Listar Estoque":
    st.subheader("📋 Produtos Cadastrados")
    df = ver_estoque()

    if df.empty:
        st.info("Nenhum produto cadastrado ainda.")
    else:
        st.dataframe(df, use_container_width=True)

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
  con = sqlite3.connect('bar.db')
  cursor = con.cursor
  st.subheader("Comandas Abertas")
  df = listar_comandas_abertas()

  if df.empyty:
    st.info("Nenhuma comanda aberta ainda.")
  else:
    st.dataframe(df, use_container_width=True)


# ------------------------
# ITENS DE UMA COMANDA ESPECÍFICA
# ------------------------

elif menu == "Itens da comanda":
   
    st.subheader("Ver os itens da comanda de um cliente")
    id_comanda = st.number_input("Digite o ID da comanda do cliente que deseja ver os itens",min_value=0,step=1)

    if st.button("Mostrar itens"):
        if id_comanda:
            df = listar_itens_comanda(id_comanda)
            st.dataframe(df,use_container_width=True)

        else:
            st.info("Coloque o ID // Sua comanda está vazia")
    
    st.info("Para encontra o ID volte no menu Comandas e procure pelo nome do cliente, assim que achar terá um número a esquerda, este é o ID!")
    con.close()
        


# ------------------------
# RESUMO
# ------------------------
elif menu == "Resumo":
    st.subheader("📊 Resumo Financeiro")

    df = listar_produtos()
    if df.empty:
        st.info("Cadastre produtos para ver o resumo.")
    else:
        df["lucro_unitario"] = df["preco_venda"] - df["preco"]
        df["lucro_total"] = df["lucro_unitario"] * df["quantidade"]