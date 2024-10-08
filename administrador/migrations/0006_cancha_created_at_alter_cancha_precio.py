# Generated by Django 5.0.6 on 2024-06-19 02:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0005_rename_esrado_favorito_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancha',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cancha',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
