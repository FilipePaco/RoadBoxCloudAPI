import uuid
from django_seed import Seed
from roadbox_cloudapi_app.models import RegS, EnvioSinistro
import random
from faker import Faker

fake = Faker()

def create_regs(num_regs):
    seeder = Seed.seeder()
    seeder.add_entity(RegS, num_regs, {
        'id_sinistro': lambda x: uuid.uuid4(),
        'clima': lambda x: fake.word(),
        'temperatura': lambda x: random.uniform(15.0, 35.0),
        'luminosidade': lambda x: fake.random_element(['Noite', 'Anoitecendo', 'Amanhecendo','Dia Claro']),
        'data_hora': lambda x: fake.date_time_this_year(),
        'latitude': lambda x: random.uniform(-16.7, -16.4),  # Limita às coordenadas de Goiânia
        'longitude': lambda x: random.uniform(-49.3, -48.9)  # Limita às coordenadas de Goiânia
    })
    seeder.execute()

def create_envio_sinistros(num_envios):
    seeder = Seed.seeder()
    seeder.add_entity(EnvioSinistro, num_envios, {
        'dispositivo': lambda x: fake.user_agent()[:10],
        'foto_sinistro': lambda x: fake.image_url() + "?text=crash+cars",  # Garante imagem de carro batido
        'data_hora': lambda x: fake.date_time_this_year(),
        'latitude': lambda x: random.uniform(-16.7, -16.4),  # Limita às coordenadas de Goiânia
        'longitude': lambda x: random.uniform(-49.3, -48.9),  # Limita às coordenadas de Goiânia
        'id_sinistro': lambda x: random.choice(RegS.objects.all())
    })
    seeder.execute()

# Popula o banco de dados
create_envio_sinistros(10)
create_regs(10)

print("Dados populados com sucesso usando Django Seed.")
