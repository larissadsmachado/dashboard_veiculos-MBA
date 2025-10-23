#app.py

import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração inicial
st.set_page_config(page_title="Valorização de Veículos no Brasil", page_icon="🚘", layout="wide")
st.title("🚘 Análise da valorização de veículos novos e usados (2020–2024)")

# Função para carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("tabela-fipe-historico-precos.csv", sep=",")
    df = df[['marca', 'modelo', 'anoModelo', 'mesReferencia', 'anoReferencia', 'valor']]
    df['data'] = pd.to_datetime(df['anoReferencia'].astype(str) + '-' + df['mesReferencia'].astype(str) + '-01')
    df = df[df['valor'] > 0]
    return df

df = load_data()

# SIDEBAR – filtros
st.sidebar.header("🔎 Filtros")
marcas_disponiveis = sorted(df['marca'].unique())
anos_disponiveis = sorted(df['anoModelo'].unique())

marcas_default = [m for m in ["Toyota", "Volkswagen", "Honda"] if m in marcas_disponiveis]
anos_default = [a for a in [2020, 2021, 2022, 2023, 2024] if a in anos_disponiveis]

marcas = st.sidebar.multiselect("Marcas", marcas_disponiveis, default=marcas_default)
anos = st.sidebar.multiselect("Ano do modelo", anos_disponiveis, default=anos_default)

df_filtrado = df[df['marca'].isin(marcas) & df['anoModelo'].isin(anos)]

# KPIs
st.subheader("📊 Indicadores principais")
col1, col2, col3 = st.columns(3)
col1.metric("Modelos avaliados", df_filtrado['modelo'].nunique())
col2.metric("Preço médio (R$)", f"{df_filtrado['valor'].mean():,.2f}")
col3.metric("Período", f"{df_filtrado['data'].min().year}–{df_filtrado['data'].max().year}")

# EVOLUÇÃO DE PREÇOS
st.markdown("### 📈 Evolução do preço médio por modelo")
modelo = st.selectbox("Selecione o modelo", sorted(df_filtrado['modelo'].unique()))
df_modelo = df_filtrado[df_filtrado['modelo'] == modelo].sort_values('data')

fig1 = px.line(df_modelo, x='data', y='valor', color='marca',
               markers=True, title=f"Evolução de preço do {modelo}")
st.plotly_chart(fig1, use_container_width=True)
st.caption("➡️ Mostra a flutuação de preços ao longo do tempo, útil para identificar valorização ou quedas sazonais.")

# TOP 10 VALORIZADOS
st.markdown("### 🏆 Top 10 modelos mais valorizados")
df_valoriz = df_filtrado.groupby('modelo').agg(
    valor_inicial=('valor', 'first'),
    valor_final=('valor', 'last')
).reset_index()
df_valoriz['% valorização'] = ((df_valoriz['valor_final'] - df_valoriz['valor_inicial']) / df_valoriz['valor_inicial']) * 100
df_top = df_valoriz.sort_values('% valorização', ascending=False).head(10)

fig2 = px.bar(df_top, x='modelo', y='% valorização', color='% valorização', text='% valorização',
              title="Top 10 modelos que mais valorizaram (%)")
st.plotly_chart(fig2, use_container_width=True)
st.caption("➡️ Ajuda a entender quais modelos mantêm valor — bom para investimento ou revenda.")

# NOVO x USADO
st.markdown("### ⚖️ Comparativo entre veículos novos e usados")
df_filtrado['tipo'] = df_filtrado['anoModelo'].apply(lambda x: 'Novo' if x >= 2024 else 'Usado')
df_tipo = df_filtrado.groupby('tipo')['valor'].mean().reset_index()

fig3 = px.bar(df_tipo, x='tipo', y='valor', color='tipo', title="Preço médio: novos vs usados")
st.plotly_chart(fig3, use_container_width=True)
st.caption("➡️ Mostra o quanto o mercado de usados vem se aproximando dos novos em valor médio.")

# INSIGHT FINAL
st.info("""
💡 **Conclusão:**  
Entre 2020 e 2024, houve valorização atípica em modelos populares usados, 
reflexo da escassez de semicondutores e aumento de demanda pós-pandemia.  
Esse padrão sugere que o mercado de usados ganhou força e estabilidade no período analisado.
""")
