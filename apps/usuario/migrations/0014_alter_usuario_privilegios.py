# Generated by Django 4.2.16 on 2024-11-14 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0013_alter_usuario_imagen_alter_usuario_privilegios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='privilegios',
            field=models.CharField(default='Usuario', max_length=15, verbose_name='Privilegios'),
        ),
    ]
