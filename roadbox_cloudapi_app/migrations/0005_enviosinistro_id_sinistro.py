# Generated by Django 5.1.2 on 2024-12-14 01:20

import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadbox_cloudapi_app', '0004_remove_enviosinistro_id_sinistro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enviosinistro',
            name='id_sinistro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='envios', to='roadbox_cloudapi_app.regs'),
        ),
         
    ]