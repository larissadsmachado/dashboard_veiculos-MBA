import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import load_data, get_filters

# Configuração da página
st.set_page_config(
    page_title="Dashboard Vendas Automóveis - Brasil",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar dados
df = load_data()

if df.empty:
    st.stop()

# Título principal
st.title("🚗 Dashboard de Vendas de Automóveis - Brasil")
st.markdown("**Análise do Mercado Automotivo Brasileiro baseada em dados da ANFAVEA**")

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

# Obter opções para filtros
marcas, modelos, regioes, estados, combustiveis, anos = get_filters(df)

# Filtros
marca_selecionada = st.sidebar.multiselect("Marca", marcas, default=marcas)
modelo_selecionado = st.sidebar.multiselect("Modelo", modelos, default=modelos)
regiao_selecionada = st.sidebar.multiselect("Região", regioes, default=regioes)
estado_selecionado = st.sidebar.multiselect("Estado", estados, default=estados)
combustivel_selecionado = st.sidebar.multiselect("Combustível", combustiveis, default=combustiveis)
ano_selecionado = st.sidebar.multiselect("Ano", anos, default=anos)

# Aplicar filtros
df_filtrado = df[
    (df['marca'].isin(marca_selecionada)) &
    (df['modelo'].isin(modelo_selecionado)) &
    (df['regiao'].isin(regiao_selecionada)) &
    (df['estado'].isin(estado_selecionado)) &
    (df['combustivel'].isin(combustivel_selecionado)) &
    (df['ano'].isin(ano_selecionado))
]

# Storytelling - Introdução
st.markdown("""
## 📖 Análise do Mercado Automotivo Brasileiro

**Problemática:** A indústria automotiva brasileira enfrenta desafios significativos com a flutuação de vendas, 
mudanças nas preferências dos consumidores e variações regionais. Este dashboard visa identificar padrões de vendas, 
comportamento do mercado e oportunidades de crescimento.

**Objetivo:** Fornecer insights estratégicos para tomada de decisão sobre investimentos, mix de produtos 
e expansão regional.
""")

# Métricas principais
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

# Gráficos
st.markdown("---")
st.header("📈 Análise de Vendas")

# Layout com duas colunas para gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Evolução Mensal de Vendas")
    
    # Agrupar por mês
    vendas_mensais = df_filtrado.groupby('mes_ano').agg({
        'vendas': 'sum',
        'faturamento': 'sum'
    }).reset_index()
    
    fig_vendas = px.line(
        vendas_mensais, 
        x='mes_ano', 
        y='vendas',
        title='Evolução das Vendas ao Longo do Tempo',
        labels={'mes_ano': 'Mês/Ano', 'vendas': 'Quantidade de Vendas'}
    )
    fig_vendas.update_layout(height=400)
    st.plotly_chart(fig_vendas, use_container_width=True)
    
    # Explicação do gráfico
    with st.expander("ℹ️ Por que analisar a evolução mensal?"):
        st.markdown("""
        **Objetivo:** Identificar sazonalidades e tendências ao longo do tempo.
        **Insights esperados:**
        - Períodos de alta e baixa nas vendas
        - Efeito de campanhas promocionais
        - Impacto de fatores econômicos
        - Sazonalidade do mercado automotivo
        """)

with col2:
    st.subheader("🏭 Vendas por Marca")
    
    vendas_marca = df_filtrado.groupby('marca').agg({
        'vendas': 'sum',
        'faturamento': 'sum'
    }).reset_index().sort_values('vendas', ascending=False)
    
    fig_marca = px.bar(
        vendas_marca.head(10),
        x='marca',
        y='vendas',
        title='Top 10 Marcas por Volume de Vendas',
        color='vendas',
        color_continuous_scale='blues'
    )
    fig_marca.update_layout(height=400)
    st.plotly_chart(fig_marca, use_container_width=True)
    
    # Explicação do gráfico
    with st.expander("ℹ️ Por que analisar vendas por marca?"):
        st.markdown("""
        **Objetivo:** Entender a participação de mercado das diferentes marcas.
        **Insights esperados:**
        - Líderes de mercado
        - Oportunidades para marcas menores
        - Estratégia de posicionamento
        - Potencial para parcerias
        """)

# Segunda linha de gráficos
col3, col4 = st.columns(2)

with col3:
    st.subheader("🗺️ Distribuição por Região")
    
    vendas_regiao = df_filtrado.groupby('regiao').agg({
        'vendas': 'sum',
        'faturamento': 'sum'
    }).reset_index()
    
    fig_regiao = px.pie(
        vendas_regiao,
        values='vendas',
        names='regiao',
        title='Distribuição de Vendas por Região',
        hole=0.4
    )
    fig_regiao.update_layout(height=400)
    st.plotly_chart(fig_regiao, use_container_width=True)
    
    # Explicação do gráfico
    with st.expander("ℹ️ Por que analisar a distribuição regional?"):
        st.markdown("""
        **Objetivo:** Identificar oportunidades de expansão regional.
        **Insights esperados:**
        - Regiões com maior potencial
        - Necessidade de ajuste na distribuição
        - Estratégias regionais específicas
        - Logística e infraestrutura necessária
        """)

with col4:
    st.subheader("⛽ Tipo de Combustível")
    
    vendas_combustivel = df_filtrado.groupby('combustivel').agg({
        'vendas': 'sum',
        'preco_medio': 'mean'
    }).reset_index()
    
    fig_combustivel = px.bar(
        vendas_combustivel,
        x='combustivel',
        y='vendas',
        title='Vendas por Tipo de Combustível',
        color='preco_medio',
        color_continuous_scale='viridis'
    )
    fig_combustivel.update_layout(height=400)
    st.plotly_chart(fig_combustivel, use_container_width=True)
    
    # Explicação do gráfico
    with st.expander("ℹ️ Por que analisar tipos de combustível?"):
        st.markdown("""
        **Objetivo:** Entender as preferências dos consumidores por tipo de combustível.
        **Insights esperados:**
        - Tendências de mercado (flex, elétricos, etc.)
        - Preços médios por categoria
        - Oportunidades para veículos sustentáveis
        - Planejamento de mix de produtos
        """)

# Análise de preços
st.markdown("---")
st.header("💰 Análise de Preços e Faturamento")

col5, col6 = st.columns(2)

with col5:
    st.subheader("📊 Preço Médio por Marca")
    
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
        title='Relação entre Preço Médio e Volume de Vendas',
        labels={'preco_medio': 'Preço Médio (R$)', 'vendas': 'Volume de Vendas'}
    )
    fig_preco.update_layout(height=500)
    st.plotly_chart(fig_preco, use_container_width=True)

with col6:
    st.subheader("🏆 Top 10 Modelos Mais Vendidos")
    
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
        title='Top 10 Modelos por Volume de Vendas',
        labels={'vendas': 'Total de Vendas', 'preco_medio': 'Preço Médio'}
    )
    fig_modelos.update_layout(height=500)
    st.plotly_chart(fig_modelos, use_container_width=True)

# Tabela detalhada
st.markdown("---")
st.header("📋 Dados Detalhados")

with st.expander("Visualizar Dados Filtrados"):
    st.dataframe(
        df_filtrado.sort_values('vendas', ascending=False),
        use_container_width=True
    )

# Conclusões e Insights
st.markdown("---")
st.header("💡 Principais Insights e Recomendações")

col7, col8 = st.columns(2)

with col7:
    st.subheader("🎯 Insights Identificados")
    st.markdown("""
    1. **Sazonalidade:** Picos de vendas em determinados meses
    2. **Liderança de Mercado:** Marcas dominantes e suas estratégias
    3. **Distribuição Regional:** Concentração em regiões específicas
    4. **Preferências:** Tipos de combustível mais populares
    5. **Relação Preço-Volume:** Como o preço afeta as vendas
    """)

with col8:
    st.subheader("🚀 Recomendações Estratégicas")
    st.markdown("""
    1. **Expansão Regional:** Investir em regiões subexploradas
    2. **Mix de Produtos:** Ajustar oferta baseada em preferências
    3. **Precificação:** Estratégias competitivas de preço
    4. **Promoções:** Timing baseado na sazonalidade
    5. **Inovação:** Desenvolver produtos para tendências emergentes
    """)

# Rodapé
st.markdown("---")
st.markdown(
    "**Dashboard desenvolvido para análise do mercado automotivo brasileiro** • "
    "Dados simulados baseados em padrões da ANFAVEA • "
    "Última atualização: 2024"
)