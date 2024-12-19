from django.shortcuts import render
#link para colocar venv no docker https://pythonspeed.com/articles/activate-virtualenv-dockerfile/

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EnvioSinistro, RegS
from .utils import *
from django.shortcuts import get_object_or_404
import uuid

class ProcessarSinistroView(APIView):
    def post(self, request):
        try:
            id_envio = request.data.get("id_envio")
            envio = EnvioSinistro.objects.get(id_envio=id_envio)
            # Buscar um RegS próximo
            regs_proximo = buscar_regs_proximo(envio)

            if regs_proximo:
                # Relacionar o envio ao RegS encontrado
                envio.id_sinistro = regs_proximo
                envio.save()
                
                    # Obter todos os EnvioSinistro associados ao RegS
                envios_associados = EnvioSinistro.objects.filter(id_sinistro=regs_proximo.id_sinistro)
                
                # Calcular a média da latitude e longitude
                lat_media = sum(envio.latitude for envio in envios_associados) / len(envios_associados)
                lon_media = sum(envio.longitude for envio in envios_associados) / len(envios_associados)
                
                # Atualizar o RegS com as médias calculadas
                regs_proximo.latitude = lat_media
                regs_proximo.longitude = lon_media
                regs_proximo.save()
                message = f"Envio relacionado ao RegS existente com UUID {regs_proximo.id_sinistro}. RegS Atualizado em coordenadas"
            else:
                 # Obter informações climáticas com base na latitude e longitude do envio
                dados_clima = obter_informacoes_clima(envio.latitude, envio.longitude)

                # Verificar se a API retornou informações válidas
                if "error" not in dados_clima:
                    clima = dados_clima.get("descricao", "Desconhecido")
                    temperatura = dados_clima.get("temperatura", "N/A")
                    luminosidade = dados_clima.get("luminosidade", "Desconhecida")
                else:
                    # Valores padrão caso a API falhe
                    clima = "Desconhecido"
                    temperatura = "N/A"
                    luminosidade = "Desconhecida"

                # Criar o novo registro RegS
                novo_regs = RegS.objects.create(
                    id_sinistro=uuid.uuid4(),
                    clima=clima,
                    temperatura=temperatura,
                    luminosidade=luminosidade,
                    data_hora=envio.data_hora,
                    latitude=envio.latitude,
                    longitude=envio.longitude,
                )

                envio.id_sinistro = novo_regs
                envio.save()
                message = f"Novo RegS criado com UUID {novo_regs.id_sinistro}."

            return Response({"message": message}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ListarSinistrosView(APIView):
    def get(self, request):
        try:
            # Consultar todos os registros de EnvioSinistro
            sinistros = RegS.objects.all()
            
            # Serializar os dados manualmente (ou use um Serializer se preferir)
            sinistros_serializados = [
                {
                    "id_sinistro": sinistro.id_sinistro,
                    "latitude": sinistro.latitude,
                    "longitude": sinistro.longitude,
                    "data_hora": sinistro.data_hora,
                    "clima": sinistro.clima,
                    "temperatura": sinistro.temperatura,
                    "luminosidade": sinistro.luminosidade,                    
                }
                for sinistro in sinistros
            ]

            return Response(sinistros_serializados, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DetalharRegSView(APIView):
    def get(self, request, id_sinistro):
        try:
            # Buscar o RegS pelo ID
            regs = get_object_or_404(RegS, id_sinistro=id_sinistro)
            
            # Serializar os dados do RegS
            regs_serializado = {
                "id_sinistro": regs.id_sinistro,
                "clima": regs.clima,
                "temperatura": regs.temperatura,
                "luminosidade": regs.luminosidade,
                "data_hora": regs.data_hora,
                "latitude": regs.latitude,
                "longitude": regs.longitude,
            }

            # Buscar os EnvioSinistro relacionados
            envios = EnvioSinistro.objects.filter(id_sinistro=regs.id_sinistro)
            envios_serializados = [
                {
                    "id_envio": envio.id_envio,
                    "latitude": envio.latitude,
                    "longitude": envio.longitude,
                    "data_hora": envio.data_hora,
                    "foto_sinistro": envio.foto_sinistro,
                }
                for envio in envios
            ]

            # Combinar os dados
            resultado = {
                "regs": regs_serializado,
                "envios_relacionados": envios_serializados,
            }

            return Response(resultado, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
