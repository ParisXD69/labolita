# Generated by Django 4.2.16 on 2024-11-13 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0008_numero_ganador'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jugada',
            old_name='fecha_jugada',
            new_name='created_at',
        ),
    ]
