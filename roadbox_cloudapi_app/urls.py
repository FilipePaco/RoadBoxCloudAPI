from django.urls import path
from .views import *

urlpatterns = [
    path('processar/', ProcessarSinistroView.as_view(), name='processar_sinistro'),
    path('listar/', ListarSinistrosView.as_view(), name='listar_sinistro'),
    path('regs/<uuid:id_sinistro>/', DetalharRegSView.as_view(), name='detalhar_regs'),

]
