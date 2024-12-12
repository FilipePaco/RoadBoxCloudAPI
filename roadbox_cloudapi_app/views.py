from django.shortcuts import render

# Create your views here.
#link para colocar venv no docker https://pythonspeed.com/articles/activate-virtualenv-dockerfile/


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EnvioSinistro, RegS
import datetime

class ProcessarSinistroView(APIView):
    def post(self, request):
        try:
            ultimo_envio = EnvioSinistro.objects.latest('id_envio')
            novo_sinistro = RegS.objects.create(
                clima="Ensolarado",
                temperatura=30.0,
                luminosidade="Alta",
                data_hora=datetime.datetime.now(),
                latitude = 123.2222,
                longitude = 12.444
            )
            ultimo_envio.id_sinistro = novo_sinistro.id_sinistro
            ultimo_envio.save()
            return Response({"message": "Processo concluído com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
