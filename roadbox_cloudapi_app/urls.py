from django.urls import path
from .views import ProcessarSinistroView

urlpatterns = [
    path('processar/', ProcessarSinistroView.as_view(), name='processar_sinistro'),
]
