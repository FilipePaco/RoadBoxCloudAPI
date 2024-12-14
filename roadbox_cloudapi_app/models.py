import uuid
from django.db import models

class RegS(models.Model):
    id_sinistro = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    clima = models.CharField(max_length=50, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    luminosidade = models.CharField(max_length=20, null=True, blank=True)
    data_hora = models.DateTimeField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True,null=True)
    class Meta:
        db_table = 'regs'  # Define o nome da tabela no banco de dados
        
class EnvioSinistro(models.Model):
    id_envio = models.AutoField(primary_key=True)
    dispositivo = models.CharField(max_length=255)
    foto_sinistro = models.URLField()
    data_hora = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    id_sinistro = models.ForeignKey(
        RegS,  # Faz referência ao modelo RegS
        on_delete=models.CASCADE,  # Exclui o envio se o sinistro for deletado
        related_name="envios",  # Nome reverso para acessar os envios de um sinistro
        null=True,  # Permite que o campo seja vazio
        blank=True
    )
    class Meta:
        db_table = 'enviodesinistro'  # Define o nome da tabela no banco de dados
