import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
import requests
import json
import sqlite3

try:
    mgl = sqlite3.connect('../1_bases_tratadas/magalu.db')
except:
    mgl = sqlite3.connect('bases_tratadas/magalu.db')

df = pd.read_sql('SELECT * FROM Magazine', con=mgl)


st.title('Projeto Magazine Luiza')


# Mostrar a tabela completa
with st.expander('Tabela Magalu'):
    st.dataframe(data=df, hide_index=True)

# Analisar estatísticas descritivas para cada tipo de produto
st.subheader('Análise estatística do preço por tipo de produto')

tipos_produtos = df['Tipo'].unique()  # Obtém os tipos de produtos únicos

for tipo in tipos_produtos:
    subset = df[df['Tipo'] == tipo]
    media = subset['Preço Bruto'].mean()
    mediana = subset['Preço Bruto'].median()
    desvio = subset['Preço Bruto'].std()
    
    # Exibição dos resultados
    st.markdown(f"### {tipo}")
    st.markdown(f"- **Média**: {media:.2f}")
    st.markdown(f"- **Mediana**: {mediana:.2f}")
    st.markdown(f"- **Desvio Padrão**: {desvio:.2f}")

# Gráficos Univariados
st.subheader("Análise Univariada")

# 1. Boxplot - Preço Bruto
st.markdown("### Boxplot - Distribuição de Preços Brutos")
boxplot = px.box(df, y="Preço Bruto", title="Boxplot - Distribuição de Preços Brutos")
st.plotly_chart(boxplot, use_container_width=True)

# 2. Gráfico de Barras - Quantidade por Tipo de Produto
st.markdown("### Gráfico de Barras - Quantidade por Tipo de Produto")
quantidade_tipos = df["Tipo"].value_counts().reset_index()
quantidade_tipos.columns = ["Tipo", "Quantidade"]
grafico_barras = px.bar(
    quantidade_tipos, 
    x="Tipo", 
    y="Quantidade", 
    color="Tipo", 
    title="Quantidade de Produtos por Tipo",
    labels={"Tipo": "Tipo de Produto", "Quantidade": "Quantidade"}
)
st.plotly_chart(grafico_barras, use_container_width=True)

# 3. Gráfico de Pizza - Participação dos Tipos de Produto
st.markdown("### Gráfico de Pizza - Participação dos Tipos de Produto")
grafico_pizza = px.pie(
    quantidade_tipos, 
    names="Tipo", 
    values="Quantidade", 
    title="Distribuição dos Tipos de Produto",
    hole=0.4
)
st.plotly_chart(grafico_pizza, use_container_width=True)

# Gráficos Multivariados
st.subheader("Análise Multivariada")

# 1. Boxplot Multivariado - Preço Bruto por Tipo
st.markdown("### Boxplot - Preço Bruto por Tipo de Produto")
boxplot_multivariado = px.box(
    df, 
    x="Tipo", 
    y="Preço Bruto", 
    color="Tipo",
    title="Distribuição do Preço Bruto por Tipo de Produto",
    labels={"Preço Bruto": "Preço Bruto (R$)", "Tipo": "Tipo de Produto"}
)
st.plotly_chart(boxplot_multivariado, use_container_width=True)

# 2. Gráfico de Barras Empilhadas - Tipo de Produto por Faixa de Preço
st.markdown("### Gráfico de Barras Empilhadas - Tipo de Produto por Faixa de Preço")
bins = [0, 100, 300, 500, 1000, 5000, 10000]  # Intervalos de preço
labels = ["0-100", "101-300", "301-500", "501-1000", "1001-5000", "5001+"]
df["Faixa de Preço Bruto"] = pd.cut(df["Preço Bruto"], bins=bins, labels=labels, include_lowest=True)

faixa_preco_tipo = df.groupby(["Faixa de Preço Bruto", "Tipo"]).size().reset_index(name="Quantidade")
grafico_empilhado = px.bar(
    faixa_preco_tipo,
    x="Faixa de Preço Bruto",
    y="Quantidade",
    color="Tipo",
    title="Distribuição dos Produtos por Faixa de Preço e Tipo",
    labels={"Faixa de Preço Bruto": "Faixa de Preço (R$)", "Quantidade": "Quantidade"}
)
st.plotly_chart(grafico_empilhado, use_container_width=True)

# 3. Gráfico de Dispersão - Avaliação vs Preço Bruto
st.markdown("### Gráfico de Dispersão - Avaliação vs Preço Bruto")
grafico_dispersao = px.scatter(
    df, 
    x="Avaliação", 
    y="Preço Bruto", 
    color="Tipo", 
    title="Relação entre Avaliação e Preço Bruto por Tipo de Produto",
    labels={"Avaliação": "Avaliação", "Preço Bruto": "Preço Bruto (R$)"}
)
st.plotly_chart(grafico_dispersao, use_container_width=True)