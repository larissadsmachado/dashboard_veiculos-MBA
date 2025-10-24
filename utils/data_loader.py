import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Carrega os dados de vendas de automóveis da ANFAVEA
    """
    try:
        df = pd.read_csv('dados_anfavea_2024.csv')
        df['mes_ano'] = pd.to_datetime(df['mes_ano'])
        return df
    except FileNotFoundError:
        st.error("Arquivo 'dados_anfavea_2024.csv' não encontrado.")
        return pd.DataFrame()

def get_filters(df):
    """
    Retorna listas únicas para os filtros
    """
    marcas = sorted(df['marca'].unique())
    modelos = sorted(df['modelo'].unique())
    regioes = sorted(df['regiao'].unique())
    estados = sorted(df['estado'].unique())
    combustiveis = sorted(df['combustivel'].unique())
    categorias = sorted(df['categoria'].unique())
    anos = sorted(df['ano'].unique())
    meses = sorted(df['mes'].unique())
    
    return marcas, modelos, regioes, estados, combustiveis, categorias, anos, meses