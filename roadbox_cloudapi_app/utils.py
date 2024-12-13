import math
import uuid
from datetime import datetime, timedelta
from .models import EnvioSinistro, RegS

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



def buscar_regs_proximo(envio, limite_distancia_km=5, limite_tempo_minutos=30):
    """
    Verifica se existe um RegS próximo ao envio em tempo e localização.
    Retorna o RegS encontrado ou None.
    """
    from .models import RegS

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
