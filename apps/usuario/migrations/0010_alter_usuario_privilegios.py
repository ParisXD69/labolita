# Generated by Django 4.2.16 on 2024-11-13 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_rename_fecha_jugada_jugada_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='privilegios',
            field=models.CharField(default='Usuario', verbose_name='Privilegios'),
        ),
    ]
