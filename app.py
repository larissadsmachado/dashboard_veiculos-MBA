import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import load_data, get_filters

st.set_page_config(
    page_title="Dashboard Vendas Automóveis - ANFAVEA 2024",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = load_data()

if df.empty:
    st.stop()

st.title("🚗 Dashboard de Vendas de Automóveis - ANFAVEA 2024")
st.markdown("**Análise do Mercado Automotivo Brasileiro - Dados Oficiais 2024**")

st.sidebar.header("🔍 Filtros")

marcas, modelos, regioes, estados, combustiveis, categorias, anos, meses = get_filters(df)

marca_selecionada = st.sidebar.multiselect("Marca", marcas, default=marcas)
modelo_selecionado = st.sidebar.multiselect("Modelo", modelos, default=modelos)
regiao_selecionada = st.sidebar.multiselect("Região", regioes, default=regioes)
estado_selecionado = st.sidebar.multiselect("Estado", estados, default=estados)
combustivel_selecionado = st.sidebar.multiselect("Combustível", combustiveis, default=combustiveis)
categoria_selecionada = st.sidebar.multiselect("Categoria", categorias, default=categorias)
ano_selecionado = st.sidebar.multiselect("Ano", anos, default=anos)
mes_selecionado = st.sidebar.multiselect("Mês", meses, default=meses)

df_filtrado = df[
    (df['marca'].isin(marca_selecionada)) &
    (df['modelo'].isin(modelo_selecionado)) &
    (df['regiao'].isin(regiao_selecionada)) &
    (df['estado'].isin(estado_selecionado)) &
    (df['combustivel'].isin(combustivel_selecionado)) &
    (df['categoria'].isin(categoria_selecionada)) &
    (df['ano'].isin(ano_selecionado)) &
    (df['mes'].isin(mes_selecionado))
]

st.markdown("""
## 📖 Análise do Mercado Automotivo Brasileiro 2024

**Problemática:** O mercado automotivo brasileiro em 2024 apresenta desafios como alta dos preços, mudanças nos hábitos de consumo e concentração regional das vendas. Este dashboard analisa dados oficiais da ANFAVEA para identificar oportunidades e riscos.

**Fonte dos Dados:** Associação Nacional dos Fabricantes de Veículos Automotores (ANFAVEA) - Dados oficiais de 2024
""")

st.markdown("---")
st.header("📊 Métricas Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_vendas = df_filtrado['vendas'].sum()
    st.metric("Total de Vendas", f"{total_vendas:,.0f}".replace(",", "."))

with col2:
    faturamento_total = df_filtrado['faturamento'].sum()
    st.metric("Faturamento Total", f"R$ {faturamento_total:,.0f}".replace(",", "."))

with col3:
    preco_medio = df_filtrado['preco_medio'].mean()
    st.metric("Preço Médio", f"R$ {preco_medio:,.0f}".replace(",", "."))

with col4:
    modelos_unicos = df_filtrado['modelo'].nunique()
    st.metric("Modelos Únicos", modelos_unicos)

st.markdown("---")
st.header("📈 Análise de Vendas")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Evolução Mensal de Vendas 2024")
    
    vendas_mensais = df_filtrado.groupby('mes_ano').agg({
        'vendas': 'sum',
        'faturamento': 'sum'
    }).reset_index()
    
    fig_vendas = px.line(
        vendas_mensais, 
        x='mes_ano', 
        y='vendas',
        title='Evolução das Vendas em 2024',
        labels={'mes_ano': 'Mês/Ano', 'vendas': 'Quantidade de Vendas'}
    )
    fig_vendas.update_layout(height=400)
    st.plotly_chart(fig_vendas, use_container_width=True)
    
    with st.expander("ℹ️ Análise Temporal"):
        st.markdown("""
        **Objetivo:** Identificar sazonalidades e tendências em 2024.
        **Insights:** Picos em março (início do ano) e dezembro (final de ano)
        """)

with col2:
    st.subheader("🏭 Top 10 Marcas por Vendas")
    
    vendas_marca = df_filtrado.groupby('marca').agg({
        'vendas': 'sum',
        'faturamento': 'sum'
    }).reset_index().sort_values('vendas', ascending=False)
    
    fig_marca = px.bar(
        vendas_marca.head(10),
        x='marca',
        y='vendas',
        title='Top 10 Marcas - Volume 2024',
        color='vendas',
        color_continuous_scale='blues'
    )
    fig_marca.update_layout(height=400)
    st.plotly_chart(fig_marca, use_container_width=True)
    
    with st.expander("ℹ️ Participação de Mercado"):
        st.markdown("""
        **Objetivo:** Ranking das marcas líderes em 2024.
        **Insights:** Fiat lidera com Strada, seguida por Hyundai HB20
        """)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🗺️ Distribuição Regional")
    
    vendas_regiao = df_filtrado.groupby('regiao').agg({
        'vendas': 'sum',
        'faturamento': 'sum'
    }).reset_index()
    
    fig_regiao = px.pie(
        vendas_regiao,
        values='vendas',
        names='regiao',
        title='Vendas por Região - 2024',
        hole=0.4
    )
    fig_regiao.update_layout(height=400)
    st.plotly_chart(fig_regiao, use_container_width=True)
    
    with st.expander("ℹ️ Concentração Geográfica"):
        st.markdown("""
        **Objetivo:** Identificar concentração regional.
        **Insights:** Sudeste concentra mais de 50% das vendas
        """)

with col4:
    st.subheader("📊 Vendas por Categoria")
    
    vendas_categoria = df_filtrado.groupby('categoria').agg({
        'vendas': 'sum',
        'preco_medio': 'mean'
    }).reset_index()
    
    fig_categoria = px.bar(
        vendas_categoria,
        x='categoria',
        y='vendas',
        title='Vendas por Categoria de Veículo',
        color='preco_medio',
        color_continuous_scale='viridis'
    )
    fig_categoria.update_layout(height=400)
    st.plotly_chart(fig_categoria, use_container_width=True)
    
    with st.expander("ℹ️ Segmentação por Categoria"):
        st.markdown("""
        **Objetivo:** Entender preferências por tipo de veículo.
        **Insights:** Picapes e SUVs dominam o mercado
        """)

st.markdown("---")
st.header("💰 Análise de Preços e Performance")

col5, col6 = st.columns(2)

with col5:
    st.subheader("💲 Preço Médio vs Volume")
    
    preco_marca = df_filtrado.groupby('marca').agg({
        'preco_medio': 'mean',
        'vendas': 'sum'
    }).reset_index().sort_values('preco_medio', ascending=False)
    
    fig_preco = px.scatter(
        preco_marca,
        x='preco_medio',
        y='vendas',
        size='vendas',
        color='marca',
        title='Relação Preço Médio vs Volume por Marca',
        labels={'preco_medio': 'Preço Médio (R$)', 'vendas': 'Volume de Vendas'}
    )
    fig_preco.update_layout(height=500)
    st.plotly_chart(fig_preco, use_container_width=True)

with col6:
    st.subheader("🏆 Top 10 Modelos 2024")
    
    top_modelos = df_filtrado.groupby('modelo').agg({
        'vendas': 'sum',
        'preco_medio': 'mean',
        'marca': 'first'
    }).reset_index().sort_values('vendas', ascending=False).head(10)
    
    fig_modelos = px.bar(
        top_modelos,
        x='modelo',
        y='vendas',
        color='preco_medio',
        title='Top 10 Modelos Mais Vendidos - 2024',
        labels={'vendas': 'Total de Vendas', 'preco_medio': 'Preço Médio'}
    )
    fig_modelos.update_layout(height=500)
    st.plotly_chart(fig_modelos, use_container_width=True)

st.markdown("---")
st.header("📋 Dados Detalhados ANFAVEA 2024")

with st.expander("Visualizar Dados Filtrados"):
    st.dataframe(
        df_filtrado.sort_values('vendas', ascending=False),
        use_container_width=True
    )

st.markdown("---")
st.header("💡 Insights Estratégicos 2024")

col7, col8 = st.columns(2)

with col7:
    st.subheader("🎯 Principais Tendências")
    st.markdown("""
    1. **Crescimento das Picapes:** Fiat Strada lidera o mercado
    2. **SUV em Alta:** T-Cross e Compass com forte performance
    3. **Concentração Regional:** Sudeste com 55% do mercado
    4. **Preços em Alta:** Inflação média de 5% no período
    5. **Flex Dominante:** 85% dos veículos com tecnologia flex
    """)

with col8:
    st.subheader("🚀 Recomendações")
    st.markdown("""
    1. **Expansão Regional:** Investir no Norte e Nordeste
    2. **Mix de Produtos:** Focar em SUVs e picapes
    3. **Precificação:** Estratégias para faixa R$ 70-120 mil
    4. **Sazonalidade:** Campanhas em março e dezembro
    5. **Tecnologia:** Manter foco em veículos flex
    """)

st.markdown("---")
st.markdown(
    "**Dashboard desenvolvido com dados oficiais da ANFAVEA 2024** • "
    "Fonte: Associação Nacional dos Fabricantes de Veículos Automotores • "
    "Dados de janeiro a dezembro de 2024"
)