# Generated by Django 5.0.6 on 2024-06-18 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0004_favorito_esrado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorito',
            old_name='esrado',
            new_name='estado',
        ),
    ]
