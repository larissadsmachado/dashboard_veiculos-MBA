import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Análise da valorização de veículos novos e usados no Brasil", page_icon="🚘", layout="wide")
st.title("🚘 Análise da valorização de veículos novos e usados no Brasil")

@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_data.csv")
    df["mes"] = pd.to_datetime(df["mes"])
    return df

df = load_data()

st.sidebar.header("Filtros")
modelos = st.sidebar.multiselect("Modelos", df["modelo"].unique(), df["modelo"].unique())
tipos = st.sidebar.multiselect("Tipo (Novo/Usado)", df["tipo"].unique(), df["tipo"].unique())

df_filtrado = df[(df["modelo"].isin(modelos)) & (df["tipo"].isin(tipos))]

st.subheader("📊 Indicadores Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Modelos analisados", len(df_filtrado["modelo"].unique()))
col2.metric("Preço médio geral", f"R$ {df_filtrado['preco'].mean():,.0f}")
col3.metric("Período analisado", f"{df_filtrado['mes'].min().year} - {df_filtrado['mes'].max().year}")

st.subheader("📈 Evolução dos Preços ao Longo do Tempo")
fig1 = px.line(df_filtrado, x="mes", y="preco", color="modelo", line_dash="tipo", title="Evolução de preços: novos x usados")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("⚖️ Comparativo Novo x Usado (Preço Médio por Modelo)")
comparativo = df_filtrado.groupby(["modelo", "tipo"])["preco"].mean().reset_index()
fig2 = px.bar(comparativo, x="modelo", y="preco", color="tipo", barmode="group", title="Preço médio por modelo e tipo de veículo")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🏆 Modelos que Mais Valorizaram (Usados)")
df_usado = df[df["tipo"] == "USADO"]
df_valoriz = df_usado.groupby("modelo").apply(lambda x: (x.iloc[-1]["preco"] - x.iloc[0]["preco"]) / x.iloc[0]["preco"] * 100).reset_index()
df_valoriz.columns = ["modelo", "valorizacao_%"]
df_valoriz = df_valoriz.sort_values(by="valorizacao_%", ascending=False)
st.dataframe(df_valoriz.style.format({"valorizacao_%": "{:.1f}%"}))

fig3 = px.bar(df_valoriz, x="modelo", y="valorizacao_%", color="modelo", title="Valorização percentual dos carros usados (2020–2024)")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
### 🧭 Conclusão
Durante a pandemia e o período pós-crise dos semicondutores, observamos uma **valorização anormal dos carros usados**, especialmente em modelos populares, que chegaram a ter aumentos de até 30%.  
A estabilização dos preços começa a ocorrer a partir de 2023, quando a produção de novos veículos se normaliza.
""")
