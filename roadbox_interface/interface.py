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


def display_image(url):
    if "drive.google.com" in url:
        # Extraí o ID da imagem do URL do Google Drive
        image_id = url.split("d/")[1].split("/view")[0]
        img_url = f"https://drive.google.com/uc?export=view&id={image_id}"
        response = requests.get(img_url)
        if response.status_code == 200:
            st.image(response.content, caption="Imagem do Sinistro")
        else:
            st.warning("Erro ao carregar a imagem.")
       
    else:
        st.warning("URL não é do Google Drive."+url)
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

    # Sidebar para selecionar o RegS
    st.sidebar.title("Selecione um RegS")

    if not df.empty:
        # Tabela com todos os RegS
        st.title("Tabela de Registros de Sinistros (RegS)")
        st.dataframe(df)

        # Criar selectbox com callback para atualizar o mapa
        options = df["id_sinistro"].tolist()
        st.sidebar.selectbox(
            "Selecione o ID do RegS:",
            options,
            key="selected_reg",  # Armazena a seleção no session_state
            on_change=update_map  # Atualiza o mapa com as coordenadas
        )

        # Detalhes do RegS selecionado
        selected_id_sinistro = st.session_state.selected_reg
        if selected_id_sinistro:
            response = requests.get(f"{API_URL_DETAIL}{selected_id_sinistro}/")
            if response.status_code == 200:
                data = response.json()
                regs_data = data["regs"]

                # Exibição melhorada dos detalhes do RegS
                st.title(f"Detalhes do RegS {selected_id_sinistro}")
                st.markdown("### Informações do Sinistro")
                st.write(f"**ID do Sinistro:** {regs_data['id_sinistro']}")
                st.write(f"**Clima:** {regs_data['clima']}")
                st.write(f"**Temperatura:** {regs_data['temperatura']}°C")
                st.write(f"**Luminosidade:** {regs_data['luminosidade']}")
                st.write(f"**Data e Hora:** {regs_data['data_hora']}")
                st.write(f"**Latitude:** {regs_data['latitude']}")
                st.write(f"**Longitude:** {regs_data['longitude']}")
                update_map()

                # Exibir envios relacionados em uma tabela
                st.markdown("### Envios Relacionados")
                envios_relacionados = data["envios_relacionados"]

                if envios_relacionados:
                    envios_df = pd.DataFrame(envios_relacionados)
                    st.dataframe(envios_df)
                    for envio in envios_relacionados:
                        display_image(envio["foto_sinistro"])
                else:
                    st.warning("Nenhum envio relacionado encontrado.")

        # Atualizar o mapa interativo Pydeck
        st.write("Mapa Interativo dos Sinistros")
        view_state = pdk.ViewState(
            latitude=st.session_state.latitude,
            longitude=st.session_state.longitude,
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

    else:
        st.warning("Nenhum dado disponível para exibir no mapa.")

except requests.exceptions.RequestException as e:
    st.error(f"Erro ao buscar os dados da API: {e}")
    
    

