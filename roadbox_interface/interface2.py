import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

# Configurações iniciais do Streamlit
st.title("Mapa de Sinistros")
st.write("Visualização interativa de sinistros registrados.")

# URL do endpoint da API Django
API_URL = "http://localhost:8083/api/listar/"  # Atualize com o endereço real da API
API_URL_DETAIL = "http://localhost:8083/api/regs/"  # Endpoint de detalhes

# Inicializar valores no session_state
if "latitude" not in st.session_state:
    st.session_state.latitude = -16.619592
if "longitude" not in st.session_state:
    st.session_state.longitude = -49.255689

# Função de callback para atualizar latitude e longitude
def update_map():
    selected_id = st.session_state.selected_reg
    response = requests.get(f"{API_URL_DETAIL}{selected_id}/")
    if response.status_code == 200:
        data = response.json()
        regs_data = data["regs"]
        st.session_state.latitude = float(regs_data['latitude'])
        st.session_state.longitude = float(regs_data['longitude'])

# Fazer a requisição GET para buscar os dados
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    # Converter os dados para um DataFrame do Pandas
    df = pd.DataFrame(data)

    # Sidebar para seleção de opções
    st.sidebar.title("Opções")

    # Adicionar campos de entrada para latitude e longitude
    st.sidebar.subheader("Navegar no Mapa")
    latitude_input = st.sidebar.number_input("Latitude", value=st.session_state.latitude, format="%.6f")
    longitude_input = st.sidebar.number_input("Longitude", value=st.session_state.longitude, format="%.6f")

    # Criar selectbox para selecionar um RegS com callback
    st.sidebar.subheader("Detalhes do RegS")
    options = df["id_sinistro"].tolist()
    st.sidebar.selectbox(
        "Selecione o ID do RegS:",
        options,
        key="selected_reg",  # Armazena o valor no session_state
        on_change=update_map  # Chama a função de callback
    )

    # Exibição dos dados detalhados
    selected_id_sinistro = st.session_state.selected_reg
    if selected_id_sinistro:
        response = requests.get(f"{API_URL_DETAIL}{selected_id_sinistro}/")
        if response.status_code == 200:
            data = response.json()
            regs_data = data["regs"]

            st.title(f"Detalhes do RegS {selected_id_sinistro}")
            st.markdown("### Informações do Sinistro")
            st.write(f"**ID do Sinistro:** {regs_data['id_sinistro']}")
            st.write(f"**Clima:** {regs_data['clima']}")
            st.write(f"**Temperatura:** {regs_data['temperatura']}°C")
            st.write(f"**Luminosidade:** {regs_data['luminosidade']}")
            st.write(f"**Data e Hora:** {regs_data['data_hora']}")
            st.write(f"**Latitude:** {regs_data['latitude']}")
            st.write(f"**Longitude:** {regs_data['longitude']}")

            # Atualizar latitude e longitude no mapa
            latitude = st.session_state.latitude
            longitude = st.session_state.longitude

            # Configurar o mapa Pydeck
            st.write("Mapa Interativo dos Sinistros")
            view_state = pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=15,
                pitch=50,
            )

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            )

            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": "ID: {id_envio}\nData: {data_hora}"},
            )

            st.pydeck_chart(r)

except requests.exceptions.RequestException as e:
    st.error(f"Erro ao buscar os dados da API: {e}")
