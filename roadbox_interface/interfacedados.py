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
        fig_temp, ax_temp = plt.subplots()
        data["temperatura"] = pd.to_numeric(data["temperatura"], errors="coerce")  # Garantir valores numéricos
        data["temperatura"].dropna().plot(kind="hist", bins=15, color="skyblue", ax=ax_temp)
        ax_temp.set_title("Distribuição de Temperatura")
        ax_temp.set_xlabel("Temperatura (°C)")
        st.pyplot(fig_temp)

    # Gráfico de Luminosidade
    if "luminosidade" in data.columns:
        st.write("### Distribuição de Luminosidade")
        luminosidade_counts = data["luminosidade"].value_counts()  # Contagem de categorias
        fig_lum, ax_lum = plt.subplots()
        luminosidade_counts.plot(kind="bar", color="gold", ax=ax_lum)
        ax_lum.set_title("Distribuição de Luminosidade")
        ax_lum.set_xlabel("Categoria de Luminosidade")
        ax_lum.set_ylabel("Quantidade")
        st.pyplot(fig_lum)


    # Gráfico de Clima
    if "clima" in data.columns:
        st.write("### Distribuição de Clima")
        clima_counts = data["clima"].value_counts()
        fig_clima, ax_clima = plt.subplots()
        clima_counts.plot(kind="bar", color="lightgreen", ax=ax_clima)
        ax_clima.set_title("Ocorrências por Clima")
        ax_clima.set_ylabel("Quantidade")
        st.pyplot(fig_clima)

    # Mapa com as Coordenadas
    st.subheader("Mapa de Localizações")
    if "latitude" in data.columns and "longitude" in data.columns:
        data_map = data[["latitude", "longitude"]].dropna()
        st.map(data_map)
    else:
        st.warning("Colunas 'latitude' e 'longitude' não encontradas nos dados.")

    # Visualização da Data e Hora
    if "data_hora" in data.columns:
        st.subheader("Registros ao Longo do Tempo")
        data["data_hora"] = pd.to_datetime(data["data_hora"], errors="coerce")
        fig_time, ax_time = plt.subplots()
        data["data_hora"].dropna().dt.date.value_counts().sort_index().plot(kind="line", ax=ax_time)
        ax_time.set_title("Registros ao Longo do Tempo")
        ax_time.set_xlabel("Data")
        ax_time.set_ylabel("Número de Registros")
        st.pyplot(fig_time)

else:
    st.warning("Nenhum dado disponível. Verifique o servidor ou a API.")
