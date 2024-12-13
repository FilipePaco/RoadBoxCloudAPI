from django.shortcuts import render

# Create your views here.
#link para colocar venv no docker https://pythonspeed.com/articles/activate-virtualenv-dockerfile/


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EnvioSinistro, RegS
from utils import buscar_regs_proximo
import uuid
import datetime

class ProcessarSinistroView(APIView):
    def post(self, request):
        try:
            id_envio = request.data.get("id_envio")
            envio = EnvioSinistro.objects.get(id_envio=id_envio)


            # Buscar um RegS próximo
            regs_proximo = buscar_regs_proximo(envio)

            if regs_proximo:
                # Relacionar o envio ao RegS encontrado
                envio.id_sinistro = regs_proximo.id_sinistro
                envio.save()
                message = f"Envio relacionado ao RegS existente com UUID {regs_proximo.id_sinistro}."
            else:
                # Criar um novo RegS
                novo_regs = RegS.objects.create(
                    id_sinistro=uuid.uuid4(),
                    clima="Desconhecido",  # Pode ser ajustado
                    temperatura=25.0,  # Pode ser ajustado
                    luminosidade="Moderada",  # Pode ser ajustado
                    data_hora=envio.data_hora,
                    latitude=envio.latitude,
                    longitude=envio.longitude,
                )
                envio.id_sinistro = novo_regs.id_sinistro
                envio.save()
                message = f"Novo RegS criado com UUID {novo_regs.id_sinistro}."

            return Response({"message": message}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)