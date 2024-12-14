import math
import uuid
from datetime import datetime, timedelta

import requests
from .models import EnvioSinistro, RegS
api_key = "c851a04b1a1055e2db0008f82d274a0b"

import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Função para calcular a distância Haversine entre dois pontos geográficos
def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.
    """
    R = 6371.0  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Resultado em km



def buscar_regs_proximo(envio, limite_distancia_km=1, limite_tempo_minutos=1):
    """
    Verifica se existe um RegS próximo ao envio em tempo e localização.
    Retorna o RegS encontrado ou None.
    """
    logger.info("vai buscar regs proximo")
    # Buscar todos os RegS existentes
    regs_existentes = RegS.objects.all()

    for regs in regs_existentes:
        # Calcular a distância entre o envio e o RegS
        distancia = calcular_distancia(envio.latitude, envio.longitude, regs.latitude, regs.longitude)

        # Calcular a diferença de tempo
        tempo_diff = abs((envio.data_hora - regs.data_hora).total_seconds()) / 60  # Diferença em minutos

        # Verificar se está dentro dos limites
        if distancia <= limite_distancia_km and tempo_diff <= limite_tempo_minutos:
            return regs  # RegS encontrado

    return None  # Nenhum RegS próximo encontrado


# Função para obter informações sobre o clima
def obter_informacoes_clima(latitude, longitude, api_key=api_key):
    logger.info("Chegou na requisição a api clima")

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Completa a URL com as coordenadas e a chave da API
    complete_url = f"{base_url}appid={api_key}&lat={latitude}&lon={longitude}"

    # Faz a requisição para a API
    response = requests.get(complete_url)

    # Converte a resposta para JSON
    data = response.json()

    # Verifica se a requisição foi bem-sucedida
    if data["cod"] == 200:  # HTTP 200 significa que a requisição foi bem-sucedida
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        sys = data.get("sys", {})
        logger.info("Passou da requisição a api clima")

        # Extrai informações do clima
        temperatura = convertKelvin(main.get("temp", "N/A"))
        pressao = main.get("pressure", "N/A")
        umidade = main.get("humidity", "N/A")
        descricao_clima = weather.get("description", "N/A")
               # Extrai horários de sunrise e sunset e converte para datetime
        timezone_offset = data.get("timezone", 0)  # Offset de fuso horário
        sunrise = datetime.utcfromtimestamp(sys.get("sunrise", 0) + timezone_offset)
        
        sunset = datetime.utcfromtimestamp(sys.get("sunset", 0) + timezone_offset)
        atual = datetime.utcnow() + timedelta(seconds=timezone_offset)
        # Calcula luminosidade descritiva
        luminosidade = calcular_luminosidade_descritiva(atual, sunrise, sunset)

        # Retorna as informações
        return {
            "temperatura": temperatura,
            "pressao": pressao,
            "umidade": umidade,
            "descricao": descricao_clima,
            "luminosidade": luminosidade
        }
    else:
        return {"error": data.get("message", "Erro desconhecido")}
    
def calcular_luminosidade_descritiva(atual, sunrise, sunset):
    """
    Calcula a luminosidade de forma descritiva com base no horário atual e nos horários de nascer e pôr do sol.
    
    Retorna descrições como:
    - "Noite"
    - "Amanhecendo"
    - "Dia claro"
    - "Anoitecendo"
    
    Parâmetros:
    - atual: horário atual (datetime)
    - sunrise: horário do nascer do sol (datetime)
    - sunset: horário do pôr do sol (datetime)
    """
    if atual < sunrise:
        return "Noite"
    elif atual > sunset:
        return "Noite"
    else:
        # Período diurno
        dia_duracao = (sunset - sunrise).total_seconds()
        tempo_passado = (atual - sunrise).total_seconds()
        fracao_luz = tempo_passado / dia_duracao

        if fracao_luz <= 0.2:
            return "Amanhecendo"
        elif fracao_luz <= 0.8:
            return "Dia claro"
        else:
            return "Anoitecendo"

def convertKelvin(kelvin):
        return kelvin - 273.15