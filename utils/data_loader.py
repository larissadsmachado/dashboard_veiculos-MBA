import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Carrega os dados de vendas de automóveis
    """
    try:
        df = pd.read_csv('dados_vendas_anfavea.csv', parse_dates=['mes_ano'])
        df['ano'] = df['mes_ano'].dt.year
        df['mes'] = df['mes_ano'].dt.month
        return df
    except FileNotFoundError:
        st.error("Arquivo 'dados_vendas_anfavea.csv' não encontrado.")
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
    anos = sorted(df['ano'].unique())
    
    return marcas, modelos, regioes, estados, combustiveis, anos