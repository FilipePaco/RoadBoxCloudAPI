# Exemplo de objetos fictícios para os envios
class EnvioSinistro:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

# Função para calcular a média da latitude e longitude
def calcular_media_coordenadas(envios_associados):
    lat_media = sum(envio.latitude for envio in envios_associados) / len(envios_associados)
    lon_media = sum(envio.longitude for envio in envios_associados) / len(envios_associados)
    return lat_media, lon_media

# Criando envios fictícios para testar
envios_associados = [
    EnvioSinistro(-16.6199877,-49.2553911), #cheverny
    EnvioSinistro(-16.6194518,-49.2549612), # borracha
    EnvioSinistro(-16.6194781,-49.2547512), # escola
]

# Testando a função de cálculo de média
lat_media, lon_media = calcular_media_coordenadas(envios_associados)

print(f"Latitude média: {lat_media}")
print(f"Longitude média: {lon_media}")
