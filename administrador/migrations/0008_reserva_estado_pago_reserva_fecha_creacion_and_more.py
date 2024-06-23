# Generated by Django 5.0.6 on 2024-06-23 21:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0007_alter_cancha_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='estado_pago',
            field=models.CharField(default='Pendiente', max_length=10),
        ),
        migrations.AddField(
            model_name='reserva',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='reserva',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]