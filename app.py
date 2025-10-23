import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração inicial
st.set_page_config(page_title="Valorização de Veículos no Brasil", page_icon="🚘", layout="wide")
st.title("🚘 Análise da valorização de veículos brasileiros (2019–2025)")

# Função para carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("tabela-fipe-historico-precos.csv", sep=",")
    df = df[['marca', 'modelo', 'anoModelo', 'mesReferencia', 'anoReferencia', 'valor']]
    df['data'] = pd.to_datetime(df['anoReferencia'].astype(str) + '-' + df['mesReferencia'].astype(str) + '-01')
    df = df[df['valor'] > 0]
    # Filtra marcas brasileiras
    marcas_brasileiras = ["Chevrolet", "Volkswagen", "Fiat", "Ford", "Renault", "Honda", "Toyota", "Nissan", "Hyundai", "Jeep"]
    df = df[df['marca'].isin(marcas_brasileiras)]
    # Filtra anos de referência de 2019 a 2025
    df = df[df['anoModelo'].between(2019, 2025)]
    return df

df = load_data()

# SIDEBAR – filtros
st.sidebar.header("🔎 Filtros")
marcas = st.sidebar.multiselect("Marcas", sorted(df['marca'].unique()), default=sorted(df['marca'].unique()))
anos = st.sidebar.multiselect("Ano do modelo", sorted(df['anoModelo'].unique()), default=sorted(df['anoModelo'].unique()))

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




# INSIGHT FINAL
st.info("""
💡 **Conclusão:**  
Entre 2019 e 2025, os modelos mais recentes tendem a manter maior valor médio, 
enquanto os modelos antigos mostram maior variação de preço.  
Essa análise ajuda a entender a valorização e depreciação no mercado brasileiro de veículos.
""")
