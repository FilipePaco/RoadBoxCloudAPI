import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configurar URL da API
API_URL = "http://localhost:8083/api/listar"  # Ajuste a URL para o seu endpoint real

# Título da Aplicação
st.title("Relatório Geral de Registros - RoadBox")

# Função para Buscar Dados da API
@st.cache_data
def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"Erro ao buscar dados: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro: {e}")
        return pd.DataFrame()

# Carregar Dados
st.write("Carregando dados do servidor...")
data = fetch_data()

if not data.empty:
    # Exibir os Dados Brutos
    st.subheader("Dados Brutos")
    st.dataframe(data)

    # Visualização da Quantidade de Registros
    st.subheader("Resumo Geral")
    st.write(f"Total de Registros: {len(data)}")

    # Gráfico de Temperatura
    if "temperatura" in data.columns:
        st.write("### Temperatura dos Registros")
        st.line_chart(data["temperatura"])

    # Gráfico de Luminosidade
    if "luminosidade" in data.columns:
        st.write("### Distribuição de Luminosidade")
        st.bar_chart(data["luminosidade"].value_counts())

    # Gráfico de Clima
    if "clima" in data.columns:
        st.write("### Distribuição de Clima")
        st.bar_chart(data["clima"].value_counts())

    # Mapa com as Coordenadas
    st.subheader("Mapa de Localizações")
    if "latitude" in data.columns and "longitude" in data.columns:
        st.map(data[["latitude", "longitude"]].dropna())

    # Visualização da Data e Hora
    if "data_hora" in data.columns:
        st.subheader("Registros ao Longo do Tempo")
        # Convertendo a coluna para datetime antes de usar .dt
        data["data_hora"] = pd.to_datetime(data["data_hora"], errors='coerce')
        st.line_chart(data["data_hora"].dt.date.value_counts().sort_index())

else:
    st.warning("Nenhum dado disponível. Verifique o servidor ou a API.")
